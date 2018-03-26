"""
The GCodeInterpreter module generates layer information from GCode.
It does this by parsing the whole GCode file. On large files this can take a while and should be used from a thread.
"""
__copyright__ = "Copyright (C) 2013 David Braam - Released under terms of the AGPLv3 License"

import math
import os
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy as np
import pprint


def gcodePath(moveType, pathType, layerThickness, startPoint):
    """
    Build a gcodePath object. This used to be objects, however, this code is timing sensitive and dictionaries proved to be faster.
    """
    if layerThickness <= 0.0:
        layerThickness = 0.01
    # if profile.getProfileSetting('spiralize') == 'True':
    # 	layerThickness = profile.getProfileSettingFloat('layer_height')
    return {'moveType': [moveType],
            'pathType': pathType,
            'layerThickness': layerThickness,
            'points': [startPoint],
            'extrusion': [0.]
            }

class gcode(object):
    """
    GCode parser parses a GCode file and stores the result in layers where each layer as paths that describe the GCode.
    """
    def __init__(self):
        self.regMatch = {}
        self.layerList = None
        self.extrusionAmount = 0
        self.filename = None
        self.progressCallback = None

    def load(self, data):
        self.filename = data
        self._fileSize = os.stat(data).st_size
        gcodeFile = open(data, 'r')
        self._load(gcodeFile)
        gcodeFile.close()

    def calculateWeight(self):
        #Calculates the weight of the filament in kg
        radius = 1.75
        volumeM3 = (self.extrusionAmount * (math.pi * radius * radius)) / (1000*1000*1000)
        return volumeM3 * 1000

    def calculateCost(self):
        cost_kg = 40
        cost_meter = 4
        if cost_kg > 0.0 and cost_meter > 0.0:
            return "%.2f / %.2f" % (self.calculateWeight() * cost_kg, self.extrusionAmount / 1000 * cost_meter)
        elif cost_kg > 0.0:
            return "%.2f" % (self.calculateWeight() * cost_kg)
        elif cost_meter > 0.0:
            return "%.2f" % (self.extrusionAmount / 1000 * cost_meter)
        return None

    def _load(self, gcodeFile):
        self.layerList = []
        pos = [0.0, 0.0, 0.0]
        posOffset = [0.0, 0.0, 0.0]
        currentE = 0.0
        currentExtruder = 0
        extrudeAmountMultiply = 1.0
        absoluteE = True
        scale = 1.0
        posAbs = True
        moveType = 'travel'
        layerThickness = 0.1
        pathType = 'CUSTOM'
        currentLayer = []
        currentPath = gcodePath(moveType, pathType, layerThickness, pos)
        currentPath['extruder'] = currentExtruder

        currentLayer.append(currentPath)

        for line in gcodeFile:
            if type(line) is tuple:
                line = line[0]

            if ';' in line:
                comment = line[line.find(';')+1:].strip()

                if comment == 'infill':
                    pathType = 'INFILL'
                elif comment == 'inner perimeter':
                    pathType = 'WALL-INNER'
                elif comment == 'outer perimeter':
                    pathType = 'WALL-OUTER'
                elif comment == 'skirt':
                    pathType = 'SKIRT'
                elif comment == 'move to next layer':
                    pathType = 'LAYER'
                elif comment == 'solid layer':
                    pathType = 'SOLID LAYER'
                elif comment == 'perimeter':
                    pathType = 'PERIMETER'

                if comment.startswith('move to next layer'):
                    currentPath = gcodePath(moveType, pathType, layerThickness, currentPath['points'][-1])
                    layerThickness = 0.0
                    currentPath['extruder'] = currentExtruder
                    for path in currentLayer:
                        path['points'] = np.array(path['points'], np.float32)
                        path['extrusion'] = np.array(path['extrusion'], np.float32)
                    self.layerList.append(currentLayer)
                    if self.progressCallback is not None:
                        if self.progressCallback(float(gcodeFile.tell()) / float(self._fileSize)):
                            #Abort the loading, we can safely return as the results here will be discarded
                            return
                    currentLayer = [currentPath]

            line = line[0:line.find(';')]

            G = getCodeInt(line, 'G')
            if G is not None:
                if G == 0 or G == 1:	#Move
                    x = getCodeFloat(line, 'X')
                    y = getCodeFloat(line, 'Y')
                    z = getCodeFloat(line, 'Z')
                    e = getCodeFloat(line, 'E')
                    f = getCodeFloat(line, 'F')
                    oldPos = pos
                    pos = pos[:]
                    if posAbs:
                        if x is not None:
                            pos[0] = x * scale + posOffset[0]
                        if y is not None:
                            pos[1] = y * scale + posOffset[1]
                        if z is not None:
                            pos[2] = z * scale + posOffset[2]
                    else:
                        if x is not None:
                            pos[0] += x * scale
                        if y is not None:
                            pos[1] += y * scale
                        if z is not None:
                            pos[2] += z * scale

                    if e is not None:
                        if absoluteE:
                            e -= currentE
                        if e > 0.:
                            moveType = 'extrude'
                        elif e < 0.:
                            moveType = 'retract'
                        else:
                            moveType = 'travel'
                    else:
                        e = 0.
                        moveType = 'else'

                    currentE += e

                    # if moveType == 'move' and oldPos[2] != pos[2]:
                    #     if oldPos[2] > pos[2] and abs(oldPos[2] - pos[2]) > 5.0 and pos[2] < 1.0:
                    #         oldPos[2] = 0.0
                    #     if layerThickness == 0.0:
                    #         layerThickness = abs(oldPos[2] - pos[2])
                    #         print(layerThickness)

                    if currentPath['moveType'] != 'retract' and currentPath['moveType'] != 'else':
                        if currentPath['moveType'] != moveType or currentPath['pathType'] != pathType: # TODO
                            currentPath = gcodePath(moveType, pathType, layerThickness, currentPath['points'][-1])
                            currentPath['extruder'] = currentExtruder
                            currentLayer.append(currentPath)

                        currentPath['points'].append(pos)
                        currentPath['moveType'].append(moveType)
                        currentPath['extrusion'].append(e * extrudeAmountMultiply)

                elif G == 4: #Delay
                    S = getCodeFloat(line, 'S')
                    P = getCodeFloat(line, 'P')
                elif G == 10: #Retract
                    currentPath = gcodePath('retract', pathType, layerThickness, currentPath['points'][-1])
                    currentPath['extruder'] = currentExtruder
                    currentLayer.append(currentPath)
                    currentPath['points'].append(currentPath['points'][0])
                elif G == 11:	#Push back after retract
                    pass
                elif G == 20:	#Units are inches
                    scale = 25.4
                elif G == 21:	#Units are mm
                    scale = 1.0
                elif G == 28:	#Home
                    x = getCodeFloat(line, 'X')
                    y = getCodeFloat(line, 'Y')
                    z = getCodeFloat(line, 'Z')
                    center = [0.0, 0.0, 0.0]
                    if x is None and y is None and z is None:
                        pos = center
                    else:
                        pos = pos[:]
                        if x is not None:
                            pos[0] = center[0]
                        if y is not None:
                            pos[1] = center[1]
                        if z is not None:
                            pos[2] = center[2]
                elif G == 29:	#Probe Z
                    pos[2] = 0.0
                elif G == 90:	#Absolute position
                    posAbs = True
                elif G == 91:	#Relative position
                    posAbs = False
                elif G == 92:
                    x = getCodeFloat(line, 'X')
                    y = getCodeFloat(line, 'Y')
                    z = getCodeFloat(line, 'Z')
                    e = getCodeFloat(line, 'E')
                    if e is not None:
                        currentE = e
                    if x is not None:
                        posOffset[0] = pos[0] - x
                    if y is not None:
                        posOffset[1] = pos[1] - y
                    if z is not None:
                        posOffset[2] = pos[2] - z
                else:
                    print("Unknown G code:" + str(G))
            else:
                M = getCodeInt(line, 'M')
                if M is not None:
                    if M == 0:	#Message with possible wait (ignored)
                        pass
                    elif M == 1:	#Message with possible wait (ignored)
                        pass
                    elif M == 25:	#Stop SD printing
                        pass
                    elif M == 80:	#Enable power supply
                        pass
                    elif M == 81:	#Suicide/disable power supply
                        pass
                    elif M == 82:   #Absolute E
                        absoluteE = True
                    elif M == 83:   #Relative E
                        absoluteE = False
                    elif M == 84:	#Disable step drivers
                        pass
                    elif M == 92:	#Set steps per unit
                        pass
                    elif M == 101:	#Enable extruder
                        pass
                    elif M == 103:	#Disable extruder
                        pass
                    elif M == 104:	#Set temperature, no wait
                        pass
                    elif M == 105:	#Get temperature
                        pass
                    elif M == 106:	#Enable fan
                        pass
                    elif M == 107:	#Disable fan
                        pass
                    elif M == 108:	#Extruder RPM (these should not be in the final GCode, but they are)
                        pass
                    elif M == 109:	#Set temperature, wait
                        pass
                    elif M == 110:	#Reset N counter
                        pass
                    elif M == 113:	#Extruder PWM (these should not be in the final GCode, but they are)
                        pass
                    elif M == 117:	#LCD message
                        pass
                    elif M == 140:	#Set bed temperature
                        pass
                    elif M == 190:	#Set bed temperature & wait
                        pass
                    elif M == 203:	#Set maximum feedrate
                        pass
                    elif M == 204:	#Set default acceleration
                        pass
                    elif M == 400:	#Wait for current moves to finish
                        pass
                    elif M == 221:	#Extrude amount multiplier
                        s = getCodeFloat(line, 'S')
                        if s is not None:
                            extrudeAmountMultiply = s / 100.0
                    else:
                        print("Unknown M code:" + str(M))
                else:
                    T = getCodeInt(line, 'T')
                    if T is not None:
                        if currentExtruder > 0:
                            posOffset[0] -= 0#profile.getMachineSettingFloat('extruder_offset_x%d' % (currentExtruder)) # TODO
                            posOffset[1] -= 0#profile.getMachineSettingFloat('extruder_offset_y%d' % (currentExtruder))
                        currentExtruder = T
                        if currentExtruder > 0:
                            posOffset[0] += 0#profile.getMachineSettingFloat('extruder_offset_x%d' % (currentExtruder))
                            posOffset[1] += 0#profile.getMachineSettingFloat('extruder_offset_y%d' % (currentExtruder))

        for path in currentLayer:
            path['points'] = np.array(path['points'], np.float32)
            path['extrusion'] = np.array(path['extrusion'], np.float32)
        self.layerList.append(currentLayer)
        if self.progressCallback is not None and self._fileSize > 0:
            self.progressCallback(float(gcodeFile.tell()) / float(self._fileSize))


def getCodeInt(line, code):
    n = line.find(code) + 1
    if n < 1:
        return None
    m = line.find(' ', n)
    try:
        if m < 0:
            return int(line[n:])
        return int(line[n:m])
    except:
        return None

def eFloat(line, code):
    n = line.find(code) + 1
    if n < 1:
        return None
    m = line.find(' ', n)
    try:
        if m < 0:
            return float(line[n:])
        return float(line[n:m])
    except:
        return None


def getCodeFloat(line, code):
    n = line.find(code) + 1
    if n < 1:
        return None
    m = line.find(' ', n)
    try:
        if m < 0:
            return float(line[n:])
        return float(line[n:m])
    except:
        return None

if __name__ == '__main__':
    t = time.time()
    g = gcode()

    filename = 'test.gcode' #'first layer height test.gcode'
    g.load(filename)

    all_layers = dict()
    all_layer_all_segments = dict()
    segments_in_layer = dict()

    infill_xpoints, infill_ypoints, infill_zpoints = [], [], []
    perimeter_xpoints, perimeter_ypoints, perimeter_zpoints = [], [], []
    skirt_xpoints, skirt_ypoints, skirt_zpoints = [], [], []
    layer_xpoints, layer_ypoints, layer_zpoints = [], [], []

    layer_count = 0

    for layer in g.layerList:
        infill_segment_coordinates, skirt_segment_coordinates, perimeter_segment_coordinates = {'x': [], 'y': [], 'z': []}, {'x': [], 'y': [], 'z': []}, {'x': [], 'y': [], 'z': []}
        x, y, z = [], [], []
        layer_coordinates = dict()
        layer_count += 1

        for moves in range(len(layer)):
            if layer[moves]['pathType'] == 'SKIRT':
                _, moveType = zip(*zip(layer[moves]['points'], layer[moves]['moveType']))
                xx, yy, zz = zip(*layer[moves]['points'])
                for ix, iy, iz, im in zip(xx, yy, zz, moveType):
                    if im == 'extrude':
                        x.append(ix), y.append(iy), z.append(iz)
                skirt_segment_coordinates['x'].extend(x), skirt_segment_coordinates['y'].extend(y), skirt_segment_coordinates['z'].extend(z)
                x, y, z, xx, yy, zz, moveType = [], [], [], [], [], [], []
                segments_in_layer.update({str(moves): {'path_type': layer[moves]['pathType'], 'path_coordinates': skirt_segment_coordinates}})

            if layer[moves]['pathType'] == 'INFILL':
                _, moveType = zip(*zip(layer[moves]['points'], layer[moves]['moveType']))
                xx, yy, zz = zip(*layer[moves]['points'])
                for ix, iy, iz, im in zip(xx, yy, zz, moveType):
                    if im == 'extrude':
                        x.append(ix), y.append(iy), z.append(iz)
                infill_segment_coordinates['x'].extend(x), infill_segment_coordinates['y'].extend(y), infill_segment_coordinates['z'].extend(z)
                x, y, z, xx, yy, zz, moveType = [], [], [], [], [], [], []
                segments_in_layer.update({str(moves): {'path_type': layer[moves]['pathType'], 'path_coordinates': infill_segment_coordinates}})

            if layer[moves]['pathType'] == 'PERIMETER':
                _, moveType = zip(*zip(layer[moves]['points'], layer[moves]['moveType']))
                xx, yy, zz = zip(*layer[moves]['points'])
                for ix, iy, iz, im in zip(xx, yy, zz, moveType):
                    if im == 'extrude':
                        x.append(ix), y.append(iy), z.append(iz)
                perimeter_segment_coordinates['x'].extend(x), perimeter_segment_coordinates['y'].extend(y), perimeter_segment_coordinates['z'].extend(z)
                x, y, z, xx, yy, zz, moveType = [], [], [], [], [], [], []
                segments_in_layer.update({str(moves): {'path_type': layer[moves]['pathType'], 'path_coordinates': perimeter_segment_coordinates}})

        layer_coordinates = dict(zip(['INFILL', 'PERIMETER', 'SKIRT'], [infill_segment_coordinates, perimeter_segment_coordinates, skirt_segment_coordinates]))
        all_layers.update({str(layer_count): layer_coordinates})
        all_layer_all_segments.update({str(layer_count): segments_in_layer})

        infill_xpoints, infill_ypoints, infill_zpoints = [], [], []
        perimeter_xpoints, perimeter_ypoints, perimeter_zpoints = [], [], []
        skirt_xpoints, skirt_ypoints, skirt_zpoints = [], [], []
        segments_in_layer = dict()


    for layer_number in range(1, len(all_layers)):

        from mpl_toolkits.mplot3d import axes3d
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        plt.xlim((-40, 40))
        plt.ylim((-40, 40))


        try:
            ax.plot_wireframe(all_layers[str(layer_number)]['INFILL']['x'][:-1],
                    all_layers[str(layer_number)]['INFILL']['y'][:-1],
                    all_layers[str(layer_number)]['INFILL']['z'][:-1], color='blue', linewidth = 0.2)
        except KeyError:
            pass
        try:
            ax.plot_wireframe(all_layers[str(layer_number)]['PERIMETER']['x'][:-1],
                    all_layers[str(layer_number)]['PERIMETER']['y'][:-1],
                    all_layers[str(layer_number)]['PERIMETER']['z'][:-1], color='green', linewidth = 0.2)
        except KeyError:
            pass
        try:
            ax.plot_wireframe(all_layers[str(layer_number)]['SKIRT']['x'][:-1],
                    all_layers[str(layer_number)]['SKIRT']['y'][:-1],
                    all_layers[str(layer_number)]['SKIRT']['z'][:-1], color='red', linewidth = 0.2)
        except KeyError:
            pass

        ax.set_zlim((0, 30))
        ax.set_title('Layer No.' + str(layer_number) + ' of the parsed ' + filename + ' file')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.savefig(str(layer_number)+'.png', orientation='portrait', transparent=False, frameon=None, dpi=500)

        # from mpl_toolkits.mplot3d import axes3d
        # import matplotlib.pyplot as plt
        # from matplotlib import cm
        #
        # fig = plt.figure()
        # ax = fig.gca(projection='3d')
        #
        # try:
        #     ax.plot_surface(all_layers[str(layer_number)]['INFILL']['x'][:-1],
        #             all_layers[str(layer_number)]['INFILL']['y'][:-1],
        #             all_layers[str(layer_number)]['INFILL']['z'][:-1], color='blue')
        # except ZeroDivisionError:
        #     pass
        # try:
        #     ax.plot_surface(all_layers[str(layer_number)]['PERIMETER']['x'][:-1],
        #             all_layers[str(layer_number)]['PERIMETER']['y'][:-1],
        #             all_layers[str(layer_number)]['PERIMETER']['z'][:-1], color='green')
        # except ZeroDivisionError:
        #     pass
        # try:
        #     ax.plot_surface(all_layers[str(layer_number)]['SKIRT']['x'][:-1],
        #             all_layers[str(layer_number)]['SKIRT']['y'][:-1],
        #             all_layers[str(layer_number)]['SKIRT']['z'][:-1], color='red')
        # except ZeroDivisionError:
        #     pass
        #
        # plt.show()
        # ax.set_title('Layer No.' + str(layer_number) + ' of the parsed ' + filename + ' file')
        # plt.gca().set_aspect('equal', adjustable='box')
        # plt.savefig(str(layer_number)+'.png', orientation='portrait', transparent=False, frameon=None, dpi=500)


    print(time.time() - t)



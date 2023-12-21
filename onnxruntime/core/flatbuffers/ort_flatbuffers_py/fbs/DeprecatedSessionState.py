# automatically generated by the FlatBuffers compiler, do not modify

# namespace: fbs

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

# deprecated: no longer using kernel def hashes
class DeprecatedSessionState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsDeprecatedSessionState(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = DeprecatedSessionState()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def DeprecatedSessionStateBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x4F\x52\x54\x4D", size_prefixed=size_prefixed)

    # DeprecatedSessionState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # DeprecatedSessionState
    def Kernels(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Indirect(o + self._tab.Pos)
            from ort_flatbuffers_py.fbs.DeprecatedKernelCreateInfos import DeprecatedKernelCreateInfos
            obj = DeprecatedKernelCreateInfos()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DeprecatedSessionState
    def SubGraphSessionStates(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from ort_flatbuffers_py.fbs.DeprecatedSubGraphSessionState import DeprecatedSubGraphSessionState
            obj = DeprecatedSubGraphSessionState()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # DeprecatedSessionState
    def SubGraphSessionStatesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

    # DeprecatedSessionState
    def SubGraphSessionStatesIsNone(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        return o == 0

def DeprecatedSessionStateStart(builder): builder.StartObject(2)
def DeprecatedSessionStateAddKernels(builder, kernels): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(kernels), 0)
def DeprecatedSessionStateAddSubGraphSessionStates(builder, subGraphSessionStates): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(subGraphSessionStates), 0)
def DeprecatedSessionStateStartSubGraphSessionStatesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def DeprecatedSessionStateEnd(builder): return builder.EndObject()

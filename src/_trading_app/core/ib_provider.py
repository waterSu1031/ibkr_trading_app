from ib_insync import IB

_ib_instance: IB = IB()

def set_ib(ib: IB):
    global _ib_instance
    _ib_instance = ib

def get_ib() -> IB:
    if _ib_instance is None:
        raise RuntimeError("IB 객체가 아직 초기화되지 않았습니다.")
    return _ib_instance
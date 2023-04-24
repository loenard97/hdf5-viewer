from enum import Enum, auto


class H5DatasetType(Enum):
    Unknown = auto()
    String = auto()
    Array1D = auto()
    Array2D = auto()
    ImageRGB = auto()
    Table = auto()

    @classmethod
    def from_numpy_array(cls, array):
        # print(array.dtype, len(array.shape), array.size)
        match array.dtype, len(array.shape), array.size:
            case arr_type, _, _ if str(arr_type).startswith("|S"):
                return cls.String
            case "int32" | "int64" | "float32" | "float64", 1, _:
                return cls.Array1D
            case "int32" | "int64" | "float32" | "float64", 2, _:
                return cls.Array2D
            case "int32" | "int64" | "float32" | "float64", 2, size if size < 100:
                return cls.Table
            case "int32" | "int64" | "float32" | "float64", 3, _:
                return cls.ImageRGB
            case _:
                return cls.Unknown
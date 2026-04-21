from app.models import CursoModel, FechaModel, HojaDeResolucionResponse
from app.preprocessing.loader import load_image
from app.preprocessing.normalizer import adaptive_threshold, to_grayscale
from app.preprocessing.perspective import correct_perspective
from app.extractors.dni import DniExtractor
from app.extractors.fecha import FechaExtractor
from app.extractors.curso import CursoExtractor
from app.extractors.respuestas import RespuestasExtractor


def process_image(raw_bytes: bytes) -> HojaDeResolucionResponse:
    all_warnings: list[str] = []

    img = load_image(raw_bytes)
    gray = to_grayscale(img)

    warped_gray, warnings = correct_perspective(gray)
    all_warnings.extend(warnings)

    thresh = adaptive_threshold(warped_gray)

    dni_data, w = DniExtractor().extract(thresh)
    all_warnings.extend(w)

    fecha_data, w = FechaExtractor().extract(thresh)
    all_warnings.extend(w)

    curso_data, w = CursoExtractor().extract(thresh)
    all_warnings.extend(w)

    respuestas_data, w = RespuestasExtractor().extract(thresh)
    all_warnings.extend(w)

    fecha = fecha_data["fecha"]
    curso = curso_data["curso"]

    return HojaDeResolucionResponse(
        dni=dni_data["dni"],
        fecha=FechaModel(
            dia=fecha["dia"],
            mes=fecha["mes"],
            anio=fecha["anio"],
        ),
        curso=CursoModel(
            tipo=curso["tipo"],
            c1=curso["c1"],
            c2=curso["c2"],
            c3=curso["c3"],
        ),
        respuestas=respuestas_data["respuestas"],
        warnings=all_warnings,
    )

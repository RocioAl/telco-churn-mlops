"""Convierte una sesión interactiva de Python (>>> y ...) de TXT a Word.
Sin marcadores: código negro, comentarios verdes, salidas azules y errores rojos.
"""
import re
import tokenize
from io import StringIO
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ================= CONFIGURACIÓN =================
ARCHIVO_ENTRADA = 'transcripcion_python.txt'       # TXT que contiene el ejercicio.
ARCHIVO_SALIDA = 'transcripcion_python.docx'      # Word que se generará.
TITULO = 'Evidencia de práctica de Python'        # Encabezado del documento.
FUENTE = 'Consolas'                               # Fuente de ancho fijo.
TAMANO_FUENTE = 9                                 # Tamaño de texto.
FONDO_TERMINAL = 'F2F4F7'                         # Fondo gris claro.
# =================================================

COLORES = {                                       # Colores de cada tipo de contenido.
    'codigo': RGBColor(0, 0, 0),                 # Código en negro.
    'salida': RGBColor(30, 90, 190),             # Resultados en azul.
    'comentario': RGBColor(24, 125, 65),        # Comentarios en verde.
    'error': RGBColor(190, 45, 45),             # Errores en rojo.
}
PATRON_REPL = re.compile(r'^\s*(>>>|\.\.\.)\s?')
PATRON_ERROR = re.compile(r'\b(?:Traceback \(most recent call last\)|[A-Za-z_]\w*(?:Error|Exception):|KeyboardInterrupt|SystemExit)\b')


def fragmentos_codigo(linea):
    """Colorea comentarios Python usando tokenize, respetando # dentro de strings."""
    try:
        tokens = list(tokenize.generate_tokens(StringIO(linea + '\n').readline))
        comentarios = [t for t in tokens if t.type == tokenize.COMMENT]
    except (tokenize.TokenError, IndentationError, SyntaxError):
        comentarios = []
    if comentarios:
        inicio = comentarios[0].start[1]
        return [(linea[:inicio], 'codigo'), (linea[inicio:], 'comentario')]
    return [(linea, 'codigo')]


def sombrear(parrafo):
    propiedades = parrafo._p.get_or_add_pPr()
    sombreado = OxmlElement('w:shd')
    sombreado.set(qn('w:fill'), FONDO_TERMINAL)
    propiedades.append(sombreado)


def agregar_linea(documento, linea, tipo):
    parrafo = documento.add_paragraph()
    parrafo.paragraph_format.space_after = Pt(0)
    parrafo.paragraph_format.line_spacing = 1.05
    sombrear(parrafo)
    partes = fragmentos_codigo(linea) if tipo == 'codigo' else [(linea, tipo)]
    for contenido, clase in partes:
        run = parrafo.add_run(contenido if contenido else ' ')
        run.font.name = FUENTE
        run.font.size = Pt(TAMANO_FUENTE)
        run.font.color.rgb = COLORES[clase]
        run.bold = clase == 'codigo'


def convertir(entrada, salida, titulo):
    texto = entrada.read_text(encoding='utf-8-sig')
    documento = Document()
    seccion = documento.sections[0]
    seccion.top_margin = Inches(0.75)
    seccion.bottom_margin = Inches(0.75)
    documento.add_heading(titulo, level=1)
    en_traceback = False
    for linea in texto.splitlines():
        repl = PATRON_REPL.match(linea)
        if repl:
            en_traceback = False
            tipo = 'codigo'
        elif linea.lstrip().startswith('Traceback (most recent call last):'):
            en_traceback = True
            tipo = 'error'
        elif en_traceback:
            tipo = 'error'
            if re.match(r'^\S*(?:Error|Exception):|^KeyboardInterrupt$|^SystemExit:', linea):
                en_traceback = False
        else:
            tipo = 'salida'
        agregar_linea(documento, linea, tipo)
    salida.parent.mkdir(parents=True, exist_ok=True)
    documento.save(salida)
    print(f'Documento generado: {salida.resolve()}')


def main():
    carpeta = Path(__file__).resolve().parent
    entrada = Path(ARCHIVO_ENTRADA)
    salida = Path(ARCHIVO_SALIDA)
    if not entrada.is_absolute():
        entrada = carpeta / entrada
    if not salida.is_absolute():
        salida = carpeta / salida
    if not entrada.is_file():
        raise FileNotFoundError(f'No existe el TXT: {entrada}')
    convertir(entrada, salida, TITULO)


if __name__ == '__main__':
    main()
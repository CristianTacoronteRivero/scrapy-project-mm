import logging
from logging.handlers import TimedRotatingFileHandler
import os, fnmatch
import traceback

def create_logging(name_file: str, path_folder: str = os.getcwd(), run_function: bool = True):
    """Funcion que crea y configura los registros para un archivo determinado

    :param name_file: nombre del fichero
    :type name_file: str
    :param path_folder: path el cual se empieza a buscar el archivo, por defecto es os.getcwd()
    :type path_folder: str, opcional
    """

    def search_path_file(name_file: str, path_folder: str = os.getcwd()) -> str:
        """Algoritmo que genera el path relativo del archivo

        :param name_file: nombre del archivo
        :type name_file: str
        :param path_folder: path el cual se empieza a buscar el archivo, por defecto es os.getcwd()
        :type path_folder: str, opcional
        :raises ValueError: error 1 -> el nombre del archivo se encuentra duplicado en el path_folder
        :raises ValueError: error 2 -> no se encuentra el archivo especificado
        :return: path relativo del archivo
        :rtype: str
        """
        ruta_absoluta = list()
        # Buscar el arhivo name_file
        for ruta, carpetas, archivos in os.walk(path_folder):
            for archivo in archivos:
                if fnmatch.fnmatch(archivo, name_file):
                    ruta = os.path.abspath(os.path.join(ruta, archivo))
                    ruta_absoluta.append(ruta)
        # en el caso de que haya mas de un archivo
        if len(ruta_absoluta) > 1:
            raise ValueError(f"Error en el fichero {name_file}: Hay mas de un archivo con el nombre {name_file}. Por vador, modifique el nombre")
        # o ninguno... se lanza un error
        elif len(ruta_absoluta) == 0:
            raise ValueError(f"Error en el fichero {name_file}: No se ha encontrado ningun fichero con el nombre {name_file}")

        # sino, devuelve la cadena del indice 0
        return ruta_absoluta[0]

    # obtengo el nombre del fichero que crea el logging
    # obtengo su path
    path_file = search_path_file(name_file)
    # construyo el path final donde se supone que debe de estar la carpeta logs
    path_dir_logs = f"{path_file.replace(name_file, '')}logs"
    # si no existe...
    if not os.path.exists(path_dir_logs):
        os.mkdir(path_dir_logs) # creo la carpeta
    path_logging = f"{path_dir_logs}/{name_file.replace('.py','')}.log"

    if not os.path.exists(path_logging) or run_function:
        # creo el handler para el archivo
        logging_handler = TimedRotatingFileHandler(
            filename=path_logging,
            when="D",  # diario
            interval=1,  # se rota 1 archivo al dia
            backupCount=7,  # quiero ver siempre los ultimos 7 dias
        )
        # le agrego un sufijo al handler para diferenciar el de cada dia
        logging_handler.suffix = "%Y%m%d.log"

        # cofnguro el archivo .log
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging_handler],
        )

        logging.info(f"Lanzamiento del script: {name_file}")

def traceback_logging():
    trace = traceback.format_exc().splitlines()
    data = trace[-2].strip()
    line = trace[-3].split("line ")[-1]
    return line, data

# def check_argument(name, value):
#     if isinstance(value, type(None)):
#         logging.error(f"No se introdujo la variable '{name}'")
#         raise ValueError(f"Se debe de especificar {name} a traves del argumento correspondiente")
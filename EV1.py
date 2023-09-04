NOTAS = {
  0:{
    "FECHA": dt.date(2023, 6, 24),
    "CLIENTE": "x",
    "MONTO": "x",
    "DETALLES": {
        0: ("PEDIDO", "MONTO")
    }
  }
}

notas_eliminadas = set()

class FechaError(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class CampoVacioERR(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

def CampoVacio(cadena):
    if cadena.strip() == "":
        raise CampoVacioERR("Error: La cadena está vacía")

def validarFecha(fecha):
    if fecha > dt.datetime.now().date():
        raise CampoVacioERR("Error: La FECHA SOBREPASA A LA FECHA ACTUAL DEL SISTEMA")

def MostrarNota(NOTAS, FOLIO):
    FECHA = NOTAS["FECHA"]
    CLIENTE = NOTAS["CLIENTE"]
    MONTO = NOTAS["MONTO"]
    print(f"--------------------  REPORTE TABULAR  DE NOTA {FOLIO} ----------------------- ")
    print("                   FOLIO     FECHA       CLIENTE      MONTO               ")
    print(f"                     {FOLIO}     {FECHA}       {CLIENTE}           {MONTO}       ")
    print(f"------------------------------------------------------------------------\n")

def MostrarDetalles(NOTAS, FOLIO):
    print(f"--------------------  DETALLES DE LA NOTA {FOLIO} ----------------------- ")
    for pedido, monto in NOTAS["DETALLES"].values():
        print(f"               {pedido}                          {monto}                    ")

try:
    while True:
        OpcionMenu = int(input("QUÉ OPCIÓN ESCOGE\n1/REGISTRAR NOTA\n2/CONSULTAS DE NOTAS\n3/CANCELAR NOTA\n4/RECUPERAR NOTA\n5/SALIR DEL SISTEMA\n"))
        # CREAR NOTA
        if OpcionMenu == 1:
            try:
                MONTO_TOTAL = 0
                Folio = max(NOTAS.keys(), default=0) + 1
                FECHA = input("DIGITE LA FECHA DEL PEDIDO YYYY/mm/dd: ")
                CampoVacio(FECHA)
                FECHA = dt.datetime.strptime(FECHA, "%Y/%m/%d").date()
                validarFecha(FECHA)
                NOMBRE = input("CUÁL ES SU NOMBRE: ")
                CampoVacio(NOMBRE)
                DETALLES = {}
                while True:
                    LLAVE = max(DETALLES.keys(), default=0) + 1
                    SERVICIO = input("NOMBRE DEL SERVICIO: ")
                    CampoVacio(SERVICIO)
                    MONTO = input("DIGITE EL MONTO DE DINERO: ")
                    CampoVacio(MONTO)
                    MONTO_FLOAT = float(MONTO)
                    MONTO_TOTAL += MONTO_FLOAT
                    DETALLES.setdefault(LLAVE, (SERVICIO, MONTO))
                    OpcionSalida = int(input("ESOS ERAN TODOS LOS DETALLES 1/SI 2/NO: "))
                    if OpcionSalida == 1:
                        break
                NOTAS.setdefault(Folio, {})
                NOTAS.get(Folio, 0).setdefault("FECHA", FECHA)
                NOTAS.get(Folio, 0).setdefault("NOMBRE", NOMBRE)
                NOTAS.get(Folio, 0).setdefault("MONTO_TOTAL", MONTO_TOTAL)
                NOTAS.get(Folio, 0).setdefault("DETALLES", DETALLES)

            except ValueError as vr:
                print("EL VALOR QUE USTED INGRESÓ NO ES COMPATIBLE CON LO QUE SE LE PIDIÓ. INTENTE DE NUEVO")
                pass
            except FechaError as fr:
                print(fr)
                pass
            except CampoVacioERR as cr:
                print(cr)
                pass
            except Exception as e:
                print(e)
                pass

        if OpcionMenu == 2:
            try:
                while True:
                    MenuNotas = int(input("QUÉ QUIERE HACER: "))
                    # VER REPORTES POR INTERVALO DE FECHAS
                    if MenuNotas == 1:
                        try:
                            FechaMin = input("DIGITE LA FECHA DE INICIO (YYYY/mm/dd): ")
                            FechaMin = dt.datetime.strptime(FechaMin, "%Y/%m/%d").date()
                            FechaMax = input("DIGITE LA FECHA DE FIN (YYYY/MM/DD): ")
                            FechaMax = dt.datetime.strptime(FechaMax, "%Y/%m/%d").date()
                            Reportes = [folio for folio in NOTAS.keys() if FechaMin <= NOTAS[folio].get("FECHA") <= FechaMax and not(folio in notas_eliminadas)]
                            if Reportes:
                                for i in Reportes:
                                    MostrarNota(NOTAS[i], i)
                            else:
                                print("NO EXISTE NINGÚN REPORTE EN ESE INTERVALO DE FECHAS")
                            break
                        except ValueError as V:
                            print("EL VALOR QUE USTED INGRESÓ NO ES COMPATIBLE CON LO QUE SE LE PIDIÓ. INTENTE DE NUEVO")
                        except Exception as e:
                            print(e)

                    # VER REPORTES POR ID
                    if MenuNotas == 2:
                        try:
                            folio = int(input("QUÉ NOTA DESEA VER: "))
                            if folio in NOTAS and not(folio in notas_eliminadas):
                                MostrarNota(NOTAS.get(folio), folio)
                                MostrarDetalles(NOTAS.get(folio), folio)
                            else:
                                print("LA NOTA NO EXISTE O NO SE ENCUENTRA DISPONIBLE EN ESTE MOMENTO")
                            break
                        except ValueError as v:
                            print("EL VALOR QUE USTED INGRESÓ NO ES COMPATIBLE CON LO QUE SE LE PIDIÓ. INTENTE DE NUEVO")
                        except Exception:
                            print("OCURRIÓ UN ERROR. INTENTE DE NUEVO")

                    # SALIR DE MENU DE CONSULTAS
                    if MenuNotas == 3:
                        print("SALIENDO DEL MENU DE CONSULTAS EXITOSAMENTE")
                        break
            except ValueError:
                print("EL VALOR QUE USTED INGRESÓ NO ES COMPATIBLE CON LO QUE SE LE PIDIÓ. INTENTE DE NUEVO")

        # CANCELAR NOTA
        if OpcionMenu == 3:
            try:
                folio = int(input("DIGITE EL FOLIO A CANCELAR: "))
                if folio in NOTAS and not(folio in notas_eliminadas):
                    MostrarNota(NOTAS.get(folio), folio)
                    MostrarDetalles(NOTAS.get(folio), folio)
                    decision = int(input("SEGURO QUIERE CANCELARLA 1/SI 2/NO: "))
                    if decision == 1:
                        notas_eliminadas.add(folio)
                        print("LA NOTA FUE CANCELADA. VOLVIENDO AL MENÚ")
                    elif decision == 2:
                        print("LA NOTA NO FUE CANCELADA. VOLVIENDO AL MENÚ")
                else:
                    print("EL FOLIO QUE USTED PROPORCIONÓ NO SE ENCUENTRA DISPONIBLE EN ESTE MOMENTO O ES INEXISTENTE")

            except TypeError as NT:
                print(f"EL FOLIO NO EXISTE {NT}")
            except ValueError as V:
                print("EL VALOR QUE USTED INGRESÓ NO ES COMPATIBLE CON LO QUE SE LE PIDIÓ. INTENTE DE NUEVO")
            except Exception as e:
                print(e)

        # RECUPERACIÓN DE NOTAS
        if OpcionMenu == 4:
            try:
                for folio in notas_eliminadas:
                    MostrarNota(NOTAS.get(folio), folio)
                decision = int(input("DESEA RECUPERAR ALGUNA NOTA 1/SI 2/NO: "))
                if decision == 1:
                    folio = int(input("QUÉ NOTA DESEA RECUPERAR: "))
                    if folio in notas_eliminadas:
                        MostrarDetalles(NOTAS.get(folio), folio)
                        decision = input("SEGURO 1/SI  2/NO: ")
                        if int(decision) == 1:
                            notas_eliminadas.remove(folio)
                            print("LA NOTA SE RECUPERÓ EXITOSAMENTE")
                        elif int(decision) == 2:
                            print("LA NOTA NO FUE RECUPERADA. SALIENDO AL MENÚ PRINCIPAL.")
                            break
                    else:
                        print("LA NOTA QUE USTED DIGITÓ NO ESTÁ ELIMINADA O NO EXISTE EN EL SISTEMA. SALIENDO AL MENÚ PRINCIPAL.")
                else:
                    print("VOLVIENDO AL MENÚ PRINCIPAL")
            except ValueError as v:
                print("EL VALOR QUE USTED INGRESÓ NO ES COMPATIBLE CON LO QUE SE LE PIDIÓ. INTENTE DE NUEVO")
            except Exception:
                print("OCURRIÓ UN ERROR. INTENTE DE NUEVO")

        # SALIDA DEL SISTEMA
        if OpcionMenu == 5:
            print("SALIENDO DEL SISTEMA")
            break
except ValueError:
    print("EL VALOR QUE USTED INGRESÓ NO ES COMPATIBLE CON LO QUE SE LE PIDIÓ. INTENTE DE NUEVO")



class DiaHoraMunicipio():
    def __init__(self, municipio, provincia, dia, rangoHoras, tiempo, temperatura):
        self.municipio = municipio
        self.provincia = provincia
        self.dia = dia
        self.rangoHoras = rangoHoras
        self.tiempo = tiempo
        self.temperatura = temperatura
        """probPrecipitacion = datos[5]
        cotaNieve = datos[6]
        tempMin = datos[7]
        tempMax = datos[8]
        dirViento = datos[9]
        velViento = datos[10]
        indiceIUV = datos[11]
        avisos = datos[12] """

    def __iter__(self):
        return iter([self.municipio, self.provincia, self.dia, self.rangoHoras, self.tiempo, self.temperatura])

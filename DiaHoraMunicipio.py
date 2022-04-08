

class DiaHoraMunicipio():
    def __init__(self, municipio, provincia, dia, rangoHoras, tiempo, temperatura, probPrecipitacion, cotaNieve, tempMin, tempMax, sensMin, sensMax):
        self.municipio = municipio.replace(",", "-")
        self.provincia = provincia
        self.dia = dia
        self.rangoHoras = rangoHoras
        self.tiempo = tiempo
        self.temperatura = temperatura
        self.probPrecipitacion = probPrecipitacion
        self.cotaNieve = cotaNieve
        self.tempMin = tempMin
        self.tempMax = tempMax
        self.sensMin = sensMin
        self.sensMax = sensMax
        """dirViento = datos[9]
        velViento = datos[10]
        indiceIUV = datos[11]
        avisos = datos[12] """

    def __iter__(self):
        return iter([self.municipio, self.provincia, self.dia, self.rangoHoras, self.tiempo, self.temperatura, self.probPrecipitacion, self.cotaNieve, self.tempMin, self.tempMax, self.sensMin, self.sensMax])

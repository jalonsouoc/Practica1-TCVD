

class DiaHoraMunicipio():
    def __init__(self, municipio, provincia, dia, rangoHoras, tiempo, temperatura, probPrecipitacion, cotaNieve, tempMin, tempMax, sensMin, sensMax, humedadMin, humedadMax, dirViento, velViento, rachaMax):
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
        self.humedadMin = humedadMin
        self.humedadMax = humedadMax
        self.dirViento = dirViento
        self.velViento = velViento
        self.rachaMax = rachaMax
        """indiceIUV = datos[11]
        avisos = datos[12] """

    def __iter__(self):
        return iter([self.municipio, self.provincia, self.dia, self.rangoHoras, self.tiempo, self.temperatura, self.probPrecipitacion, self.cotaNieve, self.tempMin, self.tempMax, self.sensMin, self.sensMax, self.humedadMin, self.humedadMax, self.dirViento, self.velViento, self.rachaMax])

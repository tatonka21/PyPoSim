from plant import SimplePlant
import pykka
from streams.Streams import globalPowerStream as powerStream


class SimplePlantActor(pykka.ThreadingActor):

    def __init__(self, id, power, fluctuation, ramp):
        super(SimplePlantActor, self).__init__()
        self.plant = SimplePlant.SimplePlant(power, fluctuation, ramp)

    def on_receive(self, message):
        if message["msg"] == "tick":
            self.plant = self.plant.evolve()
            powerStream.on_next((id, "output", self.plant.output))

        elif message["msg"] == "dispatch":
            self.plant = self.plant.dispatch(int(message["value"]))

        elif message["msg"] == "stats":
            return self.plant.output

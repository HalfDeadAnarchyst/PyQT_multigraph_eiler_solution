class Helicopter:
    def __init__(self, name, seats, fuel, the_id, v, mass_empty, mass_full, fuel_consum, time_engine,
                 koef_gsm, koef_diff, cost_service, cost_crew, cost_fuel, cost_aeno, dist_empty):
        self.name = name
        self.seats = seats      # НЕ ТРОГАТЬ!
        self.fuel = fuel        # макс. дальность
        self.the_id = the_id          # technical id
        self.curce_speed = v            # крейсерская скорость
        self.mass_empty = mass_empty    # масса пустого вертолёта
        self.mass_full = mass_full      # масса вертолёта с полной загурзкой (нормальная взлётная масса)
        self.fuel_consum = fuel_consum  # расход топлива тонн/час
        self.time_engine = time_engine  # время работы двигателя при полёта на максимальную дальность
        self.koef_gsm = koef_gsm        # коэффициент затрат на ГСМ
        self.koef_diff = koef_diff      # коэффициент диффыеренциации
        self.cost_service = cost_service    # стоимость человеко-часа работы обслуживающего персонала
        self.cost_crew = cost_crew      # стоимость человеко-часа работы экипажа
        self.cost_fuel = cost_fuel      # стоимость топлива, руб/л
        self.cost_aeno = cost_aeno      # стоимость АЭНО
        self.dist_empty = dist_empty

    def __repr__(self):
        return self.the_id

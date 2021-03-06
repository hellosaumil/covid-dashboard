from covid import Covid


# countries = covid.list_countries()
#
# italy_cases = covid.get_status_by_country_id(115)
# italy_cases = covid.get_status_by_country_name("italy")

class CovidStats():

    def __init__(self):
        self.last_covid_data = self.refresh_data()

    def refresh_data(self):
        return Covid()

    def world_data(self):
        return self.last_covid_data.get_data()

    def list_countries(self):
        return self.last_covid_data.list_countries()

    def country_stat(self, country_name=None, country_id=-1, refresh=False):
        covid = self.refresh_data() if refresh else self.last_covid_data

        if country_id != -1:
            try: return covid.get_status_by_country_id(country_id)
            except Exception:
                return {"id": "-1", "msg": "Invalid Country ID"}

        else:
            try:
                country_name = country_name.lower()
                return covid.get_status_by_country_name(country_name)

            except ValueError:
                return {"id": "-1", "msg": "Invalid Country Name"}


    def get_stats(self, refresh=False):

        covid = self.refresh_data() if refresh else self.last_covid_data

        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()

        # print("\nTotal Confirmed: {}\nActive Cases: {}\nRecovered Cases: {}\nDeaths: {}\n".format(confirmed, active, recovered, deaths))

        return { "active": active,
                "confirmed": confirmed,
                "deaths": deaths,
                "recovered": recovered
                }

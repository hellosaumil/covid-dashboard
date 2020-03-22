from covid import Covid


# countries = covid.list_countries()
#
# italy_cases = covid.get_status_by_country_id(115)
# italy_cases = covid.get_status_by_country_name("italy")

class CovidStats:

    def __init__(self):
        self.last_covid_data = self.refresh()

    def refresh_data(self):
        return Covid().get_data()

    def country_stats(self, country_name="italy", refresh=False):
        country_name = country_name.lower()

        covid = self.refresh_data() if refresh else self.last_covid_data
        return covid.get_status_by_country_name(country_name)


    def get_stats(self, refresh=False):

        covid = self.refresh_data() if refresh else self.last_covid_data

        active = covid.get_total_active_cases()
        confirmed = covid.get_total_confirmed_cases()
        recovered = covid.get_total_recovered()
        deaths = covid.get_total_deaths()

        print("\nTotal Confirmed: {}\nActive Cases: {}\nRecovered Cases: {}\nDeaths: {}\n".format(confirmed, active, recovered, deaths))

import darksky_scraper
import tkinter as tk
import tkinter.messagebox as mb

class darksky_gui:
    def __init__(self, master):
        self.master = master

        tk.Label(master, text='Latitude: ').grid(row=0, column=0, sticky='NSEW')
        self.latitude = tk.Entry(master)
        self.latitude.grid(row=0, column=1)
        
        tk.Label(master, text='Longitude: ').grid(row=1, column=0, sticky='NSEW')
        self.longitude = tk.Entry(master)
        self.longitude.grid(row=1, column=1)

        self.unit = tk.StringVar(master)
        self.unit.set('C/ms')
        tk.OptionMenu(master, self.unit, *('F/mph', 'C/ms', 'C/kmh', 'C/mph')).grid(row=2, columnspan=2, sticky='NSEW')

        tk.Button(master, text='Get Weather', command=self.get_weather).grid(row=3, columnspan=2, sticky='NSEW')

    def get_weather(self, latitude=None, longitude=None, unit=None):
        if latitude is None:
            latitude = float(self.latitude.get())
        if longitude is None:
            longitude = float(self.longitude.get())
        if unit is None:
            unit = self.unit.get()
        forecast = darksky_scraper.forecast(latitude=latitude, longitude=longitude, config_mode=unit)
        stats = forecast.get_forcast()
        print(stats.keys())
        print(stats['temperatures'].items())
        print((key.capitalize() + ': ' + str(val) for key, val in stats['temperatures'].items()))
        mb.showinfo('Current Temperature', str([key.capitalize() + ': ' + str(val) for key, val in stats['temperatures'].items()])[1:-1])


def main():
    root = tk.Tk()
    root.title('Darksky GUI')
    darksky = darksky_gui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
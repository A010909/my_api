import psutil
import os

# just for sum fun - no footprints thingy here - only funstuff because i thought it would look cool. 
class state:

    def get_ram(self):
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "ram_total" : round(memory.total/(1024**3),2),
            "ram_used" : round((memory.total-memory.available)/(1024**3),2),
            "ram_available" : round((memory.available)/(1024**3),2),
            "ram_perc_usage" : round(((memory.total-memory.available)/memory.total)*100,2),
            "swap_total" : round(swap.total/(1024**3),2),
            "swap_used" : round(swap.used/(1024**3),2),
            "swap_perc_usage" : round(swap.percent,2)
        }
    
    def get_disk(self):

        if os.name == 'posix':
            disk = psutil.disk_usage('/')
        elif os.name == 'nt':
            disk = psutil.disk_usage('C:\\')
       
        return {
            "total": round(disk.total / (1024**3),2),
            "used": round(disk.used / (1024**3),2),
            "available": round(disk.free / (1024**3),2),
            "percentage" : round(disk.percent,2)
        }
    
    def get_battery(self):
        battery = psutil.sensors_battery()
        if battery == None:
            return -1
        
        if battery.power_plugged == True:
            status = "Plugged"
        else:
            status = "Discharging"
        return {
            "battery" : battery.percent,
            "status" : status,
        }
    # I have not included cpu data becauase i dont want to deviate from the goal of making a unified digital footprint api - instead of just another btop.  


# for testing purpose only - uncomment this
# if __name__ == "__main__":
#     my_system = state()
#     print(my_system.get_ram())
#     print('\n')
#     print(my_system.get_disk())
#     print('\n')
#     print(my_system.get_battery())

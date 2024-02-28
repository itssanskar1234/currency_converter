import customtkinter
from tkinter.ttk import Combobox
import tkinter.messagebox as tmsg
import requests

class Ui(customtkinter.CTk):
    def __init__(self):
        super().__init__()


    def ui(self):
        '''Define the user interface.'''
        # Set appearance mode
        customtkinter.set_appearance_mode('Dark')

        # Define screen dimensions and position
        screen_width = 400
        screen_height = 400
        x = (self.winfo_screenwidth()- screen_width)//2
        y = (self.winfo_screenheight()- screen_height)//2 
        self.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
        self.resizable(False,False)
        self.title('Currency Converter')

        try:
            # Get currency data from API
            self.api = requests.get(f'''https://v6.exchangerate-api.com/v6/fc23f2556f67d41f058461cb/latest/USD''').json()
            self.data = dict(self.api['conversion_rates'])
            curreny_data = self.data.keys()
            self.currency_names = []
            for name in curreny_data:
                self.currency_names.append(name)

            # Create frame for UI elements
            frame = customtkinter.CTkFrame(master=self)

            # Create Combobox widgets for selecting currencies
            self.select_currency_1 = Combobox(master=frame,values=self.currency_names,width=5,height=10,font="Verdana 10")
            self.select_currency_2 = Combobox(master=frame,values=self.currency_names,width=5,height=10,font="Verdana 10")
            self.select_currency_1.set("USD") # Set default currency selection
            self.select_currency_2.set("INR")
            self.select_currency_1.bind("<<ComboboxSelected>>",self.on_text) # Bind event handler

            # Create Entry Widgets for input and output
            self.converted_val = customtkinter.StringVar()
            self.Entry_1 = customtkinter.CTkEntry(master=frame,placeholder_text=f'Enter value in {self.select_currency_1.get()}',font=("Verdana",15),width=160,fg_color='#EEE8CD',text_color='#030303',placeholder_text_color='#030303',height=30)
            self.Entry_1.bind("<Return>",self.get_data_on_enter)
            self.Entry_2 = customtkinter.CTkEntry(master=frame,font=("Verdana",15),width=160,state='disabled',textvariable=self.converted_val,fg_color='#EEE8CD',text_color='#030303',placeholder_text_color='#030303',height=30)

            # Create buttons with respective functions
            button_list = [["Switch",75,self.switch_button,0,"#DAA520"],["Convert",100,self.get_data,1,'#87CEFA'],["Clear",60,self.clear_widgets,2,"#FFFFE0"]]
            for name,Width,func,Column,color in button_list:
                create = customtkinter.CTkButton(master=frame,text=name,font=("Verdana",15,"bold"),width=Width,command=func,border_spacing=7,fg_color=color,text_color='black')
                create.grid(row=2,column=Column,pady=5,padx=5)

            # Grid placement of UI elements
            self.select_currency_1.grid(row=0,column=0,padx=5,pady=10)
            self.Entry_1.grid(row=0,column=1,padx=5,pady=10)
            self.select_currency_2.grid(row=1,column=0,padx=5,pady=10)
            self.Entry_2.grid(row=1,column=1,padx=5,pady=10)
            frame.place(x=37,y=130)

        except requests.exceptions.RequestException:
            # Handle exception for network errors
            tmsg.showerror("Error", "No internet connection or server not reachable.")
            quit()


    def on_text(self,event):
        '''Event handler for changing placeholder text.'''
        self.Entry_1.configure(placeholder_text=f"Enter value in {self.select_currency_1.get()}")


    def switch_button(self):
        '''Function to switch selected currencies.'''
        first_currency = self.select_currency_1.get()
        self.select_currency_1.set(self.select_currency_2.get())
        self.select_currency_2.set(first_currency)
        self.Entry_1.configure(placeholder_text=f"Enter value in {self.select_currency_1.get()}")



class MainAppFunctioning(Ui):
    '''Class representing the main functionality of the Currency Converter.'''
    def __init__(self):
        super().__init__()


    def get_data_on_enter(self,event):
        '''Function to fetch conversion data on pressing 'Enter'.'''
        try:
            if int(self.Entry_1.get())<0:
                tmsg.showerror("Error","Enter value in positive.")        
            else:
                data =  requests.get(f'''https://v6.exchangerate-api.com/v6/fc23f2556f67d41f058461cb/latest/{self.select_currency_1.get()}''').json()
                second_opt = data['conversion_rates'][self.select_currency_2.get()]
                get_the_value = second_opt*int(self.Entry_1.get())
                self.converted_val.set(f"{(float(get_the_value)):.2f}")

        except requests.exceptions.RequestException:
            tmsg.showerror("Error", "No internet connection or server not reachable.")
            quit()

        except ValueError:
            tmsg.showerror("Error","Enter valid input.")

        except Exception as f:
            tmsg.showerror("Error","An unknown error has occured.")


    def get_data(self):
        '''Function to fetch conversion data on pressing 'Convert' button'''
        try:
            if int(self.Entry_1.get())<0:
                tmsg.showerror("Error","Enter value in positive.")
            else:
                data =  requests.get(f'''https://v6.exchangerate-api.com/v6/fc23f2556f67d41f058461cb/latest/{self.select_currency_1.get()}''').json()
                second_opt = data['conversion_rates'][self.select_currency_2.get()]
                get_the_value = second_opt*int(self.Entry_1.get())
                self.converted_val.set(f"{(float(get_the_value)):.2f}")

        except requests.exceptions.RequestException:
            tmsg.showerror("Error", "No internet connection or server not reachable.")

        except ValueError:
            tmsg.showerror("Error","Enter valid input.")

        except Exception:
            tmsg.showerror("Error","An unknown error has occured.")


    def clear_widgets(self):
        '''Function to clear input and output widgets.'''
        self.Entry_1.delete(0,customtkinter.END)
        self.converted_val.set("")



if __name__ == "__main__":
    window = MainAppFunctioning()
    window.ui()
    window.mainloop()
import tkinter
from threading import Thread
from app.data.base import get_db_pizza, create_order


class OrderFrame(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super(OrderFrame, self).__init__(*args, **kwargs)

        self.pizza = []
        self.pizza_no = 0
        self.order_price = 0
        self.is_loading = True
        self.loading_label = tkinter.Label(self, text='Loading...')
        self.pizza_no_label = tkinter.Label(self, text='You added X pizza')
        self.order_price_label = tkinter.Label(self, text='Order costs X RON')
        self.order_btn = tkinter.Button(self, text='Order', command=self.create_order)
        self.cancel_btn = tkinter.Button(self, text='Cancel', command=self.cancel_order)
        self.ordered_pizza = []

        Thread(target=get_db_pizza, kwargs={'callback': self.set_data}).start()

    def create_order(self):
        create_order(self.ordered_pizza, self.order_price)
        self.order_price = 0
        self.pizza_no = 0
        self.update_labels()

    def set_data(self, pizza):
        self.is_loading = False
        self.pizza = pizza
        self.draw()

    def update_labels(self):
        self.pizza_no_label.configure(text=self.pizza_no if self.pizza_no > 0 else 'No pizza added')
        self.pizza_no_label.update()

        self.order_price_label.configure(text=f'{self.order_price} RON')
        self.order_price_label.update()

    def add_pizza_to_order(self, pizza):
        self.order_price += pizza.price
        self.pizza_no += 1
        self.update_labels()
        self.ordered_pizza.append(pizza.id)

    def cancel_order(self):
        self.ordered_pizza = []
        self.pizza_no = 0
        self.order_price = 0
        self.update_labels()

    def draw(self):
        if self.is_loading:
            # Add loading label if loading.
            self.loading_label.pack()
        else:
            # Remove loading label
            self.loading_label.pack_forget()

            # Add pizza elements
            for pizza_item in self.pizza:
                pizza_name_label = tkinter.Label(self, text=pizza_item.name)
                pizza_name_label.pack(side=tkinter.TOP)
                pizza_price_label = tkinter.Label(self, text=pizza_item.price)
                pizza_price_label.pack(side=tkinter.TOP)
                pizza_order_btn = tkinter.Button(self, text='Add to order', command=lambda item=pizza_item: self.add_pizza_to_order(item))
                pizza_order_btn.pack(side=tkinter.TOP)

            # Add elements to frame.
            self.pizza_no_label.pack(side=tkinter.LEFT)
            self.order_price_label.pack(side=tkinter.LEFT)
            self.order_btn.pack(side=tkinter.LEFT)
            self.cancel_btn.pack(side=tkinter.LEFT)

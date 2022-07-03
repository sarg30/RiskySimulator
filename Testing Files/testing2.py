import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.text = tk.Text(self, wrap=None)
        self.vsb = tk.Scrollbar(self, command=self.text.yview, orient="vertical")
        self.text.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.text.tag_configure("even", background="#e0e0e0")
        self.text.tag_configure("odd", background="#ffffff")

        with open(__file__, "r") as f:
            tag = "odd"
            for line in f.readlines():
                self.text.insert("end", line, tag)
                tag = "even" if tag == "odd" else "odd"


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()
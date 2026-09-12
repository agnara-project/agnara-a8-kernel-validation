from agnara import Agnara, App

app = App("test")


@app.capability(name="mycap")
def foo():
    pass


kernel = Agnara("k")
kernel.include(app)
reg = kernel.compile()
print(reg.get("test:mycap"))

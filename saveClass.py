from PIL import Image
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror


class Save():
    @staticmethod
    def save_as_image(rows, cols, grid, background):
        img = Image.new("RGB", (cols*10,rows*10), background)

        for pixel in grid:
            if pixel.color:
                for i in range(10):
                    for j in range(10):
                        img.putpixel((pixel.column*10+i, pixel.row*10+j), pixel.color)


        fileName = asksaveasfilename(filetypes=( ("Image Files", "*.png *.jpg *.jpeg"),), defaultextension="png")

        if fileName:
            try:
                img.save(fileName)
                img.show()
            except:
                showerror("Extention", "Wrong Extension")

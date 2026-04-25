import tkinter as tk

from ldclock.app import MainApp


def main() -> None:
    root = tk.Tk()
    MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

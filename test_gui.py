import tkinter as tk
import math
from gui import MainWindow


def monkeypatchCommand(monkeypatch, window, command):
    monkeypatch.setattr('gui.MainWindow.getInput', command)
    window.main("<Return>")


def closeApplication(app):
    app.master.destroy()


def test_correct_input(monkeypatch):
    def move(a):
        return 'naprzod 100'

    def turn(a):
        return 'obrot 90'

    def podnies(a):
        return 'podnies'

    def opusc(a):
        return 'opusc'

    mockFunctions = [move, turn, podnies, opusc]
    root = tk.Tk()
    window = MainWindow(root)
    for mockFunction in mockFunctions:
        monkeypatchCommand(monkeypatch, window, mockFunction)
        assert window.ui.label.cget("text") == mockFunction(window)
    closeApplication(window)


def test_incorrect_input(monkeypatch):
    def incorrect_input_undefined_command(a):
        return 'jump 100'

    def incorrect_input_index_error(a):
        return 'naprzod'

    def incorrect_input_value_error(a):
        return 'podnies 100'

    def getExample():
        return 'naprzod 100'

    undefined_command_text = 'Undefined command: jump 100\n'
    index_error_text = 'IndexError\n'
    value_error_text = 'ValueError\n'
    textList = [
        undefined_command_text,
        index_error_text,
        value_error_text
    ]
    mockFunctions = [
        incorrect_input_undefined_command,
        incorrect_input_index_error,
        incorrect_input_value_error]

    root = tk.Tk()
    window = MainWindow(root)
    for mockFunction, text in zip(mockFunctions, textList):
        monkeypatch.setattr('InputProcessing.getExample', getExample)
        monkeypatchCommand(monkeypatch, window, mockFunction)
        example = f'Example of a correct entry: {getExample()}'
        assert window.ui.label.cget("text") == text + example
    closeApplication(window)


def test_move_north(monkeypatch):
    def move(a):
        return 'naprzod 100'

    root = tk.Tk()
    window = MainWindow(root)
    image_x = window.image_x
    image_y = window.image_y
    monkeypatchCommand(monkeypatch, window, move)
    assert window.image_x == image_x
    assert window.image_y == image_y - 100
    closeApplication(window)


def test_move_east(monkeypatch):
    def turn(a):
        return 'obrot 90'

    def move(a):
        return 'naprzod 100'

    root = tk.Tk()
    window = MainWindow(root)
    image_x = window.image_x
    image_y = window.image_y
    monkeypatchCommand(monkeypatch, window, turn)
    assert window.image_x == image_x
    assert window.image_y == image_y
    monkeypatchCommand(monkeypatch, window, move)
    assert window.image_x == image_x + 100
    assert window.image_y == image_y
    closeApplication(window)


def test_move_at_angle(monkeypatch):
    def turn(a):
        return 'obrot 30'

    def move(a):
        return 'naprzod 100'

    root = tk.Tk()
    window = MainWindow(root)
    image_x = window.image_x
    image_y = window.image_y
    monkeypatchCommand(monkeypatch, window, turn)
    assert window.image_x == image_x
    assert window.image_y == image_y
    monkeypatchCommand(monkeypatch, window, move)
    move_x = 100 * math.sin(math.radians(30))
    move_y = -(100 * math.cos(math.radians(30)))
    assert round(window.image_x, 2) == round(image_x + move_x, 2)
    assert round(window.image_y, 2) == round(image_y + move_y, 2)

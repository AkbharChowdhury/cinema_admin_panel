from PyQt6.QtWidgets import QGridLayout, QWidget


class GridLayoutManager:
    @staticmethod
    def add_widgets(layout: QGridLayout, widgets: list[QWidget]) -> None:
        for column, widget in enumerate(widgets):
            layout.addWidget(widget, 0, column)

from PyQt6.QtWidgets import QGridLayout, QWidget


class GridLayoutManager:
    @staticmethod
    def add_widgets(layout: QGridLayout, widgets: list[QWidget]):
        for column, widget in enumerate(widgets):
            layout.addWidget(widget, 0, column)

    @staticmethod
    def add_widgets_custom_row(layout: QGridLayout, widgets: list[QWidget]):
        for row, widget in enumerate(widgets):
            layout.addWidget(widget, row, 0)

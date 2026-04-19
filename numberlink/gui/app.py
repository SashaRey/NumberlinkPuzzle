import sys
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
)

from numberlink.io.loader import load_text
from numberlink.io.parser import parse_puzzle
from numberlink.validation import validate_puzzle
from numberlink.geometry.factory import create_geometry
from numberlink.solver.backtracking import BacktrackingSolver

from numberlink.gui.canvas import HexCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hexagonal Numberlink")
        self.resize(800, 600)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout(self.central_widget)
        self.top_layout = QHBoxLayout()

        # Canvas
        self.canvas = HexCanvas(self)

        # Buttons
        self.btn_load = QPushButton("Load Puzzle")
        self.btn_solve = QPushButton("Solve")

        self.btn_load.clicked.connect(self.load_puzzle)
        self.btn_solve.clicked.connect(self.solve_puzzle)

        self.btn_solve.setEnabled(False)

        self.top_layout.addWidget(self.btn_load)
        self.top_layout.addWidget(self.btn_solve)
        self.top_layout.addStretch()

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addWidget(self.canvas)

        self.puzzle = None
        self.geometry = None
        self.solution_iterator = None
        self.solution_index = 0

    def load_puzzle(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Puzzle", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_path:
            return

        try:
            text = load_text(Path(file_path))
            puzzle = parse_puzzle(text)
            validate_puzzle(puzzle)
            self.puzzle = puzzle
            self.geometry = create_geometry(self.puzzle)
            self.canvas.set_puzzle(self.puzzle)
            self.btn_solve.setEnabled(True)
            self.btn_solve.setText("Solve")
            self.solution_iterator = None
            self.solution_index = 0
            self.setWindowTitle("Hexagonal Numberlink")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load puzzle:\n{e}")

    def solve_puzzle(self):
        if not self.puzzle or not self.geometry:
            return

        try:
            if self.solution_iterator is None:
                solver = BacktrackingSolver()
                self.solution_iterator = solver.iter_solutions(
                    self.puzzle, self.geometry
                )
                self.solution_index = 0

            try:
                next_solution = next(self.solution_iterator)
                self.solution_index += 1
                self.canvas.set_solution(next_solution)
                self.btn_solve.setText("Next Solution")
                self.setWindowTitle(
                    f"Hexagonal Numberlink - Solution #{self.solution_index}"
                )
            except StopIteration:
                QMessageBox.information(self, "Finished", "Больше нет решений.")
                self.btn_solve.setEnabled(False)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to solve puzzle:\n{e}")


def run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()

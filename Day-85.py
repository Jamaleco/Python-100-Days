import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget, QLineEdit, QDialog, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap, QImage, QPainter, QFont
from PyQt6.QtCore import Qt, QRect

class WatermarkDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Configurar Marca D'Água")

        self.watermark_text_input = QLineEdit(self)
        self.watermark_text_input.setPlaceholderText("Digite o texto da marca d'água")

        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.accept)

        cancel_button = QPushButton("Cancelar", self)
        cancel_button.clicked.connect(self.reject)

        layout = QHBoxLayout()
        layout.addWidget(self.watermark_text_input)
        layout.addWidget(ok_button)
        layout.addWidget(cancel_button)

        self.setLayout(layout)

    def get_watermark_text(self):
        return self.watermark_text_input.text()

class WatermarkApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_path = None

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        select_button = QPushButton("Selecionar Imagem", self)
        select_button.clicked.connect(self.select_image)

        watermark_button = QPushButton("Adicionar Marca D'Água", self)
        watermark_button.clicked.connect(self.add_watermark)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(select_button)
        layout.addWidget(watermark_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def select_image(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Imagens (*.png *.jpg *.jpeg *.gif *.bmp)")
        file_path, _ = file_dialog.getOpenFileName()

        if file_path:
            self.image_path = file_path
            self.display_image()

    def display_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap)

    def add_watermark(self):
        if self.image_path:
            watermark_dialog = WatermarkDialog(self)
            result = watermark_dialog.exec()

            if result == QDialog.DialogCode.Accepted:
                watermark_text = watermark_dialog.get_watermark_text()

                original_image = QImage(self.image_path)

                modified_image = QImage(original_image)

                font = QFont()
                font.setPixelSize(5) 

                painter = QPainter(modified_image)
                painter.setPen(Qt.GlobalColor.black)
                painter.setFont(font)

                font_metrics = painter.fontMetrics()
                text_rect = font_metrics.boundingRect(QRect(0, 0, 0, 0), Qt.AlignmentFlag.AlignLeft, watermark_text)
                x = modified_image.width() - text_rect.width() - 10  # 10 pixels da borda direita
                y = modified_image.height() - text_rect.height() - 10  # 10 pixels da borda inferior

                painter.drawText(x, y, watermark_text)

                output_path, _ = QFileDialog.getSaveFileName(self, "Salvar Imagem", "", "Imagens PNG (*.png)")

                if output_path:
                    modified_image.save(output_path)

                    self.image_path = output_path
                    self.display_image()

                    QMessageBox.information(self, "Sucesso", "Marca d'água adicionada com sucesso!")

                    sys.exit()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WatermarkApp()
    window.show()
    sys.exit(app.exec())

""" Parser pdf. """
import fitz


class Parser:
  """Parser abstract class"""
  def __init__(self, file_path: str):
    """ init """
    self.file_path = file_path

  def extract_text(self) -> dict:
    """Overrides Parser.extract_text()"""
    pass


class PdfParser(Parser):
  """PdfParser child class"""
  def __init__(self, file_path: str):
    """ init """
    super().__init__(file_path=file_path)

    self.pdf = fitz.Document(self.file_path)
    self.result_links = []

  def extract_text(self) -> dict:
    """Overrides Parser.extract_text()"""

    with open("temp/parse_file/text.txt", "w", encoding="utf-8") as f_manager:
      for page in self.pdf:
        self._add_links(page.getLinks())

        f_manager.write(page.getText())

    return {
        'result_links': self.result_links,
        'pageCount': self.pdf.pageCount,
        'metadata': self.pdf.metadata,
        'content': self.pdf.getToC(),
        'annotation': len(self.pdf) > 0 if self.pdf[0].firstAnnot else '',
    }

  def _add_links(self, links: list) -> None:
    if len(links) != 0:
      for link in links:
        if link["kind"] == fitz.LINK_URI:
          self.result_links.append(link["uri"])

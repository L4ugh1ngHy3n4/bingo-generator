// Large-print bingo cards. Data is supplied by generate.py.
#set page(paper: "a4", margin: 10mm)
#set text(font: "Libertinus Sans", weight: "bold", fill: black)
#set par(leading: 0pt)
#let cards = json("cards.json")
#let letters = ("B", "I", "N", "G", "O")
#for (index, card) in cards.enumerate() {
  if index > 0 { pagebreak() }
  table(
    columns: (1fr,) * 5,
    rows: (27mm,) + (48mm,) * 5,
    stroke: 2pt + black,
    align: center + horizon,
    inset: 0pt,
    table.header(..letters.map(letter => text(size: 60pt, letter))),
    ..card.flatten().map(number => text(size: 64pt, str(number))),
  )
}

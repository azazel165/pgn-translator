import chess.pgn
from googletrans import Translator
from argparse import ArgumentParser
import asyncio


def replaceWords(comment: str) -> str:
    words = {"obispo": "alfil", "checke": "jaque"}

    for clave, valor in words.items():
        if clave in comment:
            comment.replace(clave, valor)

    return comment


def getFileName() -> str:
    argparser = ArgumentParser()
    argparser.add_argument(
        "--filename", dest="file", type=str, required=True, help="Tu archivo pe"
    )

    return argparser.parse_args().file


trans = Translator()
filename = getFileName()


async def translatePgn(node, depth=0):
    for variation in node.variations:
        comment = variation.comment
        if variation.comment.strip():
            translatedComment = await trans.translate(comment, dest="es")
            variation.comment = replaceWords(translatedComment.text)
            print(f"Traducido: {variation.move.san()} : {variation.comment}")
        await translatePgn(variation, depth + 1)


async def main():
    output_file = "Translated - " + filename

    with (
        open(filename, encoding="utf-8") as archivoPgn,
        open(output_file, "w", encoding="utf-8") as archivoSalida,
    ):
        exporter = chess.pgn.FileExporter(archivoSalida)

        while True:
            game = chess.pgn.read_game(archivoPgn)

            if game is None:
                break
            await translatePgn(game)

            print(f" Se tradujo el capitulo: {game.headers.get('event')}")
            game.accept(exporter)

        print(f"PGN traducido guardado en: {output_file}")


asyncio.run(main())

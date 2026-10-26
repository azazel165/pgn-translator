#! /bin/python3

import chess.pgn
from googletrans import Translator
from argparse import ArgumentParser, Namespace
import asyncio


def replaceWords(comment: str) -> str:
    words = {"obispo": "alfil", "checke": "jaque"}

    for clave, valor in words.items():
        if clave in comment:
            comment.replace(clave, valor)

    return comment


def getArguments() -> Namespace:
    argparser = ArgumentParser()
    argparser.add_argument(
        "--filename", dest="file", type=str, required=True, help="Tu archivo pe"
    )
    argparser.add_argument(
        "--output", dest="output", type=str, help="Archivo de salida."
    )

    return argparser.parse_args()


args = getArguments()
trans = Translator()
filename = args.file
output_file = args.output if (args.output is not None) else "PGNTraducido.pgn"


async def translatePgn(node, depth=0):
    for variation in node.variations:
        comment = variation.comment
        if variation.comment != "":
            translatedComment = await trans.translate(comment, dest="es")
            variation.comment = replaceWords(translatedComment.text)
            print(f"Traducido: {variation.san()} : {variation.comment}")
        await translatePgn(variation, depth + 1)


async def main():

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

            print(f" Se tradujo el capitulo: {game.headers.get('Event')}")
            game.accept(exporter)

        print(f"PGN traducido guardado en: {output_file}")


asyncio.run(main())

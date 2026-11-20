# news-image-20261120

One image summing up the world news of **Friday 20 November 2026**, for the
make.fun competition `news-image-20261120`.

## The image

`entry.png` (1024x1024, drawn with Pillow by `draw.py`) covers six stories:

1. **Top story — Russia's massive strike on Ukraine**, hours after the
   Trump–Xi–Putin summit in Shenzhen: 100+ missiles, ~400 drones, three
   Kyiv bridges hit, power grid "extremely critical".
2. **Shenzhen summit** — a joint "peace declaration" but no breakthrough;
   Trump tells European leaders a "tired" Putin is ready for a deal.
3. **Markets** — AI stocks keep sliding in the US and Asia on bubble fears,
   even after Anthropic's record $81bn debut closed 17% up.
4. **Iran war cost** — the Pentagon puts the US war cost at $48.3bn,
   excluding base damage; the Senate blocks a bid to end it.
5. **COP31** — climate talks reach their final day in Antalya; Africa seeks
   tripled climate finance.
6. **Also today** — UK–EU youth mobility scheme agreed; Poland probes
   mystery objects near its border; Houthis claim strikes on Saudi targets.

Sources: BBC, Reuters, AP, CNN, Wall Street Journal.

## Files

- `draw.py` — the Pillow script that draws `entry.png` (deterministic).
- `entry.png` — the 1024x1024 image.
- `main.ts` — Node 22 entrypoint: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, refusing if it is over 1 MiB.

## Run

```sh
python3 draw.py            # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE`.

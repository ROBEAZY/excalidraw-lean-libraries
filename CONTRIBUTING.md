# Contributing

Thanks for wanting to improve these libraries. Changes come in as pull
requests; the owner (@ROBEAZY) reviews and merges.

## How the repo works

The `.excalidrawlib` files are generated, not drawn. Each library has a
Python script in `tools/` that describes every shape in code and writes the
library file plus a preview scene:

```bash
python tools/build_vsm.py .
python tools/build_charts.py .
python tools/build_asme.py .
python tools/build_lean.py .
```

Each script also validates its output: library format version 2, unique item
names, one group per item, and every text binding resolving inside its item.
Builds are deterministic, so running a script twice gives identical files.
CI reruns every generator on each pull request and fails if the committed
files differ from the regenerated ones.

## Making a change

1. Fork the repo and create a branch.
2. Edit the generator in `tools/`, not the `.excalidrawlib` file.
3. Run the generator and commit the regenerated library and preview files.
4. Open a pull request using the template. Include a screenshot of the
   changed items on an Excalidraw canvas if you can.

## What makes a good item

- Useful to more than one person, and not trivial to draw by hand.
- Grouped so it inserts as a single unit; boxes use bound text so labels edit
  in place.
- English labels and names that use the words people search for.
- Hand-drawn style: `roughness` 1, stroke `#1e1e1e`, Excalifont.
- Nothing company-specific and no personal data.

## Proposing a new library

Open an issue first with the list of items you have in mind. Libraries here
are also submitted to the public catalogue at https://libraries.excalidraw.com,
whose guidelines apply: https://github.com/excalidraw/excalidraw-libraries#guidelines

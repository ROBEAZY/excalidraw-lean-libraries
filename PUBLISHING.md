# Publishing a library to the Excalidraw catalogue

The public catalogue at https://libraries.excalidraw.com is fed from the
GitHub repo https://github.com/excalidraw/excalidraw-libraries. There is no
API: libraries are submitted from inside the Excalidraw app, and a bot opens a
pull request in that repo for the maintainers to review. One submission per
library.

## Before you start

- Read the catalogue guidelines once:
  https://github.com/excalidraw/excalidraw-libraries#guidelines
  In short: useful to others, nothing trivial, no copies of other libraries,
  English only, every item usable on its own, at least three related items,
  multi-element items grouped. All four libraries here were built to those
  rules.
- Have your author details ready: display name, GitHub username, optional
  website. They are published in the catalogue's `authors.json`.
- Use a normal browser window on https://excalidraw.com. The in-app library
  panel is per browser profile, so start with an empty personal library or be
  prepared to tick only the items that belong to the library you are
  publishing.

## Step by step

1. Open https://excalidraw.com and click the **Library** button (book icon,
   top right). The library panel opens.
2. Click the **⋮** menu next to the search box and choose **Open**. Pick the
   `.excalidrawlib` file from `libraries/` (download it from this repo first,
   or use a local clone). The items appear under *Personal Library*.
3. Hover an item: a small checkbox appears in its top-right corner. Tick it.
   Repeat for every item of the library you are publishing. Items from other
   libraries must stay unticked, or they will be submitted too. The **⋮**
   button shows a badge with the number of ticked items.
4. Click the **⋮** menu again and choose **Rename or publish**. The *Publish
   library* dialog opens.
5. The dialog lists every ticked item with its thumbnail and an **Item name**
   field. Names are pre-filled from this repo's item names; every item must
   have one, because the catalogue search indexes them. Remove a stray item
   with the red cross on its thumbnail.
6. Fill in the rest of the form:
   - **Library name** and **Library description** (both required): use the
     suggestions below, which carry the words people search for. The catalogue
     has no categories; search over name, description and item names is the
     only way people find a library.
   - **Author name** (required), **GitHub username** (optional, but it lets you
     edit the submission while it is under review), **Twitter username** and
     **Website** (both optional).
   - There is no licence checkbox: the note under the form says that by
     submitting you agree to publish under the MIT License.
   *Save name(s) and exit* only stores the item names locally; **Submit** sends
   the library.
7. Click **Submit**. The dialog confirms and links to the pull request the bot
   opened in `excalidraw/excalidraw-libraries`. Save that link. The bot
   generates the catalogue preview image from the submitted items.
8. Watch the pull request. Maintainers may ask for changes; reply on the PR.
   Review is human and slow (weeks, sometimes longer). Once merged, the library
   appears at https://libraries.excalidraw.com with a one-click install.

If you later improve a library, publish it again the same way. The bot opens a
new pull request; mention the earlier one in a comment so the maintainers can
treat it as an update.

## Suggested metadata

| File | Name | Description |
| --- | --- | --- |
| `value-stream-mapping.excalidrawlib` | Value Stream Mapping (Lean) | Standard value stream mapping (VSM) symbols for lean and six sigma work: process and data boxes, inventory, supermarket, FIFO lane, push and pull arrows, truck shipment, kanban cards and post, heijunka box, kaizen burst, timeline. Follows the Learning to See conventions. |
| `lean-six-sigma-charts.excalidrawlib` | Lean Six Sigma Charts | Problem-solving templates for lean and six sigma: PDCA cycle, DMAIC chevrons, fishbone (Ishikawa) diagram with 6M, 5 Whys ladder, Pareto chart, SIPOC table, control chart, impact/effort matrix, A3 template. Labels edit in place. |
| `asme-flow-process-chart.excalidrawlib` | ASME Flow Process Chart | ASME process chart symbols for method study and process analysis: operation, transport, inspection, delay, storage, combined operation and inspection, plus a flow process chart template, summary block and operation process chart column. Industrial engineering, work study, lean. |
| `lean-workplace.excalidrawlib` | Lean Workplace | Visual management and shop-floor lean tools: kanban board and sticky notes, andon light stack, 5S red tag and 5S cycle, RAG status indicators, spaghetti diagram paths, workstation, operator balance chart (takt vs cycle time), standard work combination sheet, hour-by-hour board, safety cross. |

## The manual alternative

If the in-app flow fails, the maintainers also accept hand-made pull requests:
fork `excalidraw/excalidraw-libraries`, add
`libraries/<your-github-name>/<library>.excalidrawlib` and a preview image
next to it, append an entry to `libraries.json` (name, description, authors,
source, preview, created, updated, version 2, a unique id), and open the PR.
The in-app flow does all of this for you, so prefer it.

## Submissions

| Library | Submitted | Pull request |
| --- | --- | --- |
| Value Stream Mapping (Lean) | 2026-10-20 | https://github.com/excalidraw/excalidraw-libraries/pull/2944 |
| Lean Six Sigma Charts | 2026-10-20 | https://github.com/excalidraw/excalidraw-libraries/pull/2945 |
| ASME Flow Process Chart | 2026-10-20 | https://github.com/excalidraw/excalidraw-libraries/pull/2946 |
| Lean Workplace | 2026-10-20 | https://github.com/excalidraw/excalidraw-libraries/pull/2947 |

All four were submitted through the in-app Publish flow with author
Robin Lawrence and GitHub username ROBEAZY. Watch the pull requests for
reviewer comments; a merged one appears at https://libraries.excalidraw.com.

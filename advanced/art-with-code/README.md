# Art with code: how Claude makes pictures, and whether a skill makes it more creative

Claude can't hold a brush. Every picture it makes comes from one of three routes:

1. **Code that draws:** a JavaScript program that colours a canvas, pixel by pixel or shape by shape.
2. **Code the graphics card runs:** a *shader*, a small program your graphics card runs once for every pixel on the screen.
3. **A mouse it can only see through screenshots:** Claude drives a paint program the way you would, a click and a drag at a time. This is called *computer use*.

This topic walks through each route and why it works, including why a whole animated 3D scene can be a smaller file than one photo. Then it asks a harder question: Claude's first idea is usually the most familiar one, so can a skill called **antialgorithm** push it somewhere less predictable? You find out by running the same prompts with and without it.

Everything here was run for real on **2026-11-20** with:

| Tool | Version |
|---|---|
| Claude Code | 2.1.329, default model |
| antialgorithm skill | upstream commit `766e304` (2026-11-18), MIT licence |
| Python | 3.13.18, with numpy 2.5.3, Pillow 12.3.0, cairosvg 2.9.1 |
| Node.js | 22.23.5 |
| Playwright | 1.63.0, with its own Chromium |
| git | 2.43.0 |

`demo/setup.sh` installs exactly that tested commit, `766e304`. The replies quoted below are the real ones from those runs. Yours will not be identical: Claude words things differently each time, and the skill rolls a random starting point on purpose.

**Time:** about 60-90 minutes for the whole topic, or about 50 minutes for the class exercise alone. **Cost:** the two coffee shop runs cost $0.08 (plain) and $0.13 (with the skill). See [What it cost](#what-it-cost).

## The idea in one paragraph

A video stores the answer: the colour of every pixel in every frame. A program stores the question: given this pixel and this moment, what colour should it be? Your browser and graphics card already contain the machinery to answer that question millions of times a second, so the file only has to describe the scene. That is why code-made art is tiny, and why Claude, which is good at writing code, can make it at all. The catch is that Claude can't see what its code draws unless you give it a way to look, so every route below comes down to the same loop: make something, look at a screenshot, fix what looks wrong.

## Before you start

You need:

- Claude Code, working and logged in.
- **A browser.** Any recent Chrome, Edge, Firefox or Safari opens the interactive page.
- **git.** Check with `git --version`.
- **Python 3** for the skill's scripts. Check with `python3 --version`. For the poster prompt the skill also wants numpy, Pillow and either `rsvg-convert` or the cairosvg package: `python3 -m pip install numpy pillow cairosvg`.
- **Node.js** if you want to run the starter prompt in Part 1, because Claude uses Playwright, a library for controlling a browser from code, to take its screenshots. Check with `node --version`. Claude Code can install Playwright itself when it needs it.

On Windows, use WSL.

## Step 1: open the interactive page

The page `demo/art-by-code.html` explains each route with a live demo: a planet drawn by a shader whose source code sits next to it, a landscape you can re-roll with a seed, and a replay of a computer use run you can step through. Open it straight from the folder:

```bash
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course/advanced/art-with-code
```

Then open `demo/art-by-code.html` in your browser (double-click it, or drag it into a browser window). On WSL, run `explorer.exe demo/art-by-code.html` to open it in your Windows browser.

It works offline. The only thing it fetches is its fonts; without a connection it falls back to your system fonts. The planet needs WebGL, which every current browser has. If your browser has it turned off, the page says so and the rest still works.

## Step 2: the build loop (route 1)

Nobody types the art in. You describe a scene and its rules, Claude writes a program, and the program paints every frame. The important part is what comes next: Claude opens the page in a *headless* browser (a real browser with no window, driven by a script), takes screenshots, looks at them and fixes what's wrong. Without that, it is coding blind.

Try it. Make a folder and start Claude Code there:

```bash
mkdir -p demo/practice/harbour
cd demo/practice/harbour
claude
```

Then paste this prompt:

```
Make a single HTML page that draws an animated night harbour with canvas code only, no image files. Every motion must loop seamlessly every 60 seconds. Make each frame depend only on the time t, and add a ?t= setting to the page address that freezes the scene at that second. Then open it with Playwright in headless Chromium, take screenshots at t=0, 20, 40 and 60, look at them, and fix anything that looks wrong. The t=60 shot should match t=0 if the loop is seamless. Repeat until you're happy, and tell me what you changed.
```

Three parts of the prompt do the work:

- **"Every motion must loop seamlessly every 60 seconds"** is a rule, and rules shape the code more than the subject does.
- **"add a ?t= setting"** lets Claude jump straight to any moment instead of waiting in real time. Without it, "a screenshot at 40 seconds" can mean waiting 40 real seconds. An earlier version of this prompt left that out and was ambiguous.
- **"Repeat until you're happy"** turns one attempt into a loop.

What happened in our run, which took two rounds:

- **Round 1:** no errors, and the t=60 screenshot matched t=0 byte for byte, so the loop was seamless. But two things looked frozen. The lighthouse beam turned exactly 6 times a minute, once every 10 seconds, so it pointed the same way at 0, 20 and 40 seconds. The clouds were spaced a third of the screen apart and moved a third every 20 seconds, so they looked the same too. Claude changed the beam to 5 turns a minute and spaced the clouds unevenly.
- **Round 2:** the beam and clouds now differ between shots, and the loop check still passed.

The result is in `sample-output/harbour/`: the page (`harbour.html`, about 10 KB), the screenshot script Claude wrote (`shoot.js`), and the screenshots at t=0, 20, 40 and 60. Notice that `t0.png` and `t60.png` are the same picture. Your harbour will look different.

## Step 3: seeds and loops

Scroll to **Seeds and loops** on the interactive page. Two ideas carry most generative art:

- **A seed makes randomness repeatable.** The page's landscape takes every "random" choice (ridge heights, sun position, colours) from a number generator started from one seed. Move the slider to 200, then back to 42: the exact same landscape returns. An artist can share "seed 42" instead of a file.
- **A whole-number loop makes animation seamless.** If every moving thing finishes an exact number of cycles per loop, the last frame leads straight back into the first. That is why the harbour's beam had to turn a whole number of times a minute.

## Step 4: why a whole 3D scene is smaller than a photo (route 2)

Scroll to the planet. It is drawn by the shader printed next to it, which the page measures as it runs: about 1.9 KB of text. Compare that with:

| | Size |
|---|---|
| The planet's shader | about 1.9 KB |
| One 1080p frame stored as raw pixels (1920 × 1080 × 4 bytes) | 8.3 MB |
| Two minutes of 1080p as a typical streaming-quality video (about 8 Mbit/s) | about 120 MB |

Three tricks keep it small:

- **Ray tracing a sphere is one formula.** For each pixel, imagine a ray from the camera through that pixel and ask whether it hits the ball. That is a school quadratic equation. No *mesh* (the triangles 3D models are usually made of) is needed.
- **Detail comes from noise, not images.** The swirls come from a *hash*: a scrambling formula that turns a position into a number that looks random but is always the same for that position. Nothing has to be saved because it can be recomputed.
- **Looks are mostly numbers.** A different look is a different set of *uniforms*, the knobs the page passes into the shader: colours, band counts, light direction. Very different looks, like an ink drawing or 8-bit pixels, add a short extra branch to the shader.

A fuller scene built the same way, with rings, a moon, a gas cloud and five looks, comes to about 25 KB: roughly 15 KB of shader, 8 KB of code that sets up the graphics card and 3 KB of settings for the looks.

Now break the loop on purpose. Set **Turns per loop** to **1.37** and click **Jump to the loop seam**. When the clock wraps from 10 back to 0, the storm spot jumps, because the planet was in the middle of a turn. Set it back to 1 or 2 and the wrap is invisible.

## Step 5: painting by cursor (route 3)

Scroll to **Painting by cursor**. Here Claude is put in front of [JS Paint](https://github.com/1j01/jspaint), a browser copy of MS Paint, and told to make a masterpiece. It gets only what a person would: a screen, a mouse and a keyboard.

The loop:

1. **Claude looks.** It asks for a screenshot (1024 × 640) or a zoomed-in view of part of the screen.
2. **Claude acts.** It sends a *tool call*, a structured request for a program to carry out, such as `left_click_drag` with start and end coordinates.
3. **A driver moves the mouse.** A small Python program turns the call into real mouse input with Playwright, inside Docker (a sealed mini-computer, or *container*) with no network.
4. **The result comes back.** A stroke returns just `"OK"`. Claude chains several strokes, then asks to look again, and repeats until it says it's finished.

Click **Play** on the replay to watch a made-up sample run, and look at the tool call that each step shows. A real call looks like this:

```json
{
  "type": "tool_use",
  "name": "left_click_drag",
  "input": { "start_coordinate": [120, 60], "coordinate": [600, 60] }
}
```

What made the real runs work, and what they cost:

- **A locked box.** The paint program ran in Docker with no network, as a user with no special permissions. Shortcuts that would close or reload the page were refused by the driver.
- **A spending cap.** Every screenshot costs *tokens*, the units the API bills by. The loop counted dollars from each reply and stopped before a set limit.
- **Notes instead of memory.** After about 30 screenshots the conversation gets heavy, so Claude wrote notes to itself and a fresh conversation started from them, with the canvas kept.
- **The numbers.** Real runs took 58 to 707 strokes, 7 to 26 minutes and $0.46 to $4.07.

You don't run this one: it needs an Anthropic API key with credit, Docker and a custom driver. The point is to see a different way of working. Code is fast and cheap but needs a program; computer use is slow and costly but works with any app a person can use.

One more thing to notice. Asked for a masterpiece with no other direction, separate runs on different models all painted the same subject: a sunset over a mountain lake. The sample replay paints one too. That is the "average pick" the next step is about.

## Step 6: the antialgorithm skill, with and without

A language model tends to produce what is most likely, given everything it has read. For a creative request, "most likely" means the middle of everything already made: the synthwave sunset poster, the mountain lake, the coffee shop called Common Grounds. It feels right because it's familiar.

[antialgorithm](https://github.com/mankidev/antialgorithm), by the developer **mankidev** (MIT licence), is a Claude Code skill that tries to push Claude off that middle. It does not add talent. It adds a procedure:

1. **Name the default.** "The default here is X." Then avoid X unless the brief demands it.
2. **Start from outside.** If the request is thin, roll a random starting point (a method, a palette, a setting, a verb) with its `seed.py` script, so two people with the same prompt start in different places. It is the seed idea from Step 3, used to pick ideas instead of pixels.
3. **Give every choice a reason.** One sentence, using a fact about this project. Odd for its own sake doesn't count.
4. **Check the work.** Its `check.py` renders an SVG and flags text that is cut off, covered, too small or low in contrast.
5. **Watch your own habits.** Its `moves.py` logs each main move, so last time's escape doesn't become this time's default.

### Setup

The setup script makes two empty practice folders and installs the skill into one of them only:

```bash
cd demo
./setup.sh
```

Expected output (your path will differ):

```
Ready:
  /home/you/ai-dev-course/advanced/art-with-code/demo/practice/plain        (no skill)
  /home/you/ai-dev-course/advanced/art-with-code/demo/practice/with-skill   (antialgorithm 766e304 in .claude/skills/antialgorithm/)
```

A skill in a folder's `.claude/skills/` is only visible to Claude Code sessions started in that folder, so `plain/` never sees it. Upstream's own install command, `git clone https://github.com/mankidev/antialgorithm ~/.claude/skills/antialgorithm`, puts it in your user-wide skills folder instead, where every session on your computer would get it, plain ones included. Don't use that for this exercise.

**Read the skill before you use it.** It runs Python scripts on your computer, so look first:

```bash
cat practice/with-skill/.claude/skills/antialgorithm/SKILL.md
ls practice/with-skill/.claude/skills/antialgorithm/scripts
```

```
check.py  history.py  moves.py  rough.py  seed.py
```

We read all five scripts. They only read and write files inside the skill's own folder and a temporary folder, render SVGs, and make no network calls.

**Check that it loaded.** Start Claude Code in each folder and ask:

```
Which skills do you have available? List their names only, one per line.
```

In `practice/with-skill`, the list includes `antialgorithm`. In `practice/plain`, it does not. (Both lists also show the skills that come with Claude Code.)

### One run, for real

We gave both folders the same prompt:

```
Suggest a name and a one-line slogan for a new coffee shop.
```

**Plain** ($0.08, 3 seconds):

> **Name:** Common Grounds
>
> **Slogan:** "Where good coffee brings good company."
>
> The name is a play on words. "Grounds" means the coffee, and "common ground" means a place where people get together.

**With the skill** ($0.13, 10 seconds):

> **Shift Change**: "Open at 5:40, when your night shift ends."
>
> The usual pick here is a coffee pun with a warm, cozy slogan, like "The Daily Grind: brewed with love." I didn't have details about your shop, so I assumed it's near a hospital or a factory. The name is a phrase those workers already use, and the slogan names who it's for: people coming off a night shift. The 5:40 opening time is made up, so swap in your real hours.
>
> What's next door to the shop, and who walks in first in the morning? That would let me fit the name to your actual customers.

The skill's procedure is visible in the reply: it named the default it was avoiding, picked a direction for a stated reason, said which detail was invented, and asked one question that would make it fit better. Whether "Shift Change" is a *better* name than "Common Grounds" is a different question, and that is what the exercise is for.

`sample-output/poster/` has a second pair, made in an earlier test with the same skill commit, for the prompt "Design a poster for a music festival as a 400x600 SVG." Plain made a purple-to-orange gradient with a striped synthwave sun and a giant centred title. The skill named that default, rolled a seed (string and pins, very pale colours, a back yard in Croatia, a lantern) and made the lineup into name tags pegged on washing lines. `check.py` caught overlapping tags, which it fixed, but one tag still ended up partly covered. Open `side-by-side.png`.

### The class exercise (about 50 minutes)

Work in pairs. One person is **Plain** and works in `practice/plain`; the other is **Skill** and works in `practice/with-skill`. You both give the same prompts, then put the results side by side, labelled, and judge them together. This is not a blind test, so each pair first writes down which side they expect to win; that shows the class its own bias.

| Time | What happens |
|---|---|
| Before class | The instructor reads the skill's files and runs the setup on a test machine. |
| 5 min | Everyone runs `./setup.sh`. Pairs pick two prompts and write down a predicted winner for each. |
| 20 min | Both partners run both prompts. Then each partner runs one of the two prompts twice more. |
| 10 min | Judge each pair of results with the table below, scoring before reading Claude's explanations. |
| 15 min | Pool the tallies on the board and discuss. |

Prompts to pick from:

```
Design a poster for a music festival as a 400x600 SVG. Save it as final.svg.
```
```
Suggest a name and a one-line slogan for a new coffee shop.
```
```
Write the opening paragraph of a short story set on a night bus.
```
```
Invent one core mechanic for a small puzzle game about gardening.
```
```
Design the home screen of a habit tracker app as a single HTML file.
```

The poster prompt is the slowest, because the skill checks its own render. Pick at most one poster per pair. If a run in `with-skill` doesn't seem to use the skill, add "Use the antialgorithm skill." to the prompt.

**Judge each pair.** Every row is "yes = good". Answer before reading what Claude says about its own choices: the skill side always explains its reasons, which would tilt the third row.

| Question | Plain | Skill |
|---|---|---|
| Is it specific to this brief, so it couldn't be pasted into another project unchanged? | yes / no | yes / no |
| Is it something most people would *not* make first? | yes / no | yes / no |
| Can you name, in one sentence, a reason its main choice fits this brief? | yes / no | yes / no |
| Does it do its job: readable, usable, on brief? (1-5) | score | score |
| How surprising is it? (1-5) | score | score |
| Which one would you actually use? | pick one | |

Rows 1 and 2 and the surprise score only measure "different". "Does it do its job" and "which would you use" measure "better". Look for results that score high on both.

**Run it again.** Plain runs one prompt two more times: do the three results look alike? That repetition is the "average pick". Skill runs the same prompt two more times: do the results share a move, such as the same paper texture or hand-drawn look? The skill itself warns that its favourite escape can turn into a new default.

**Hand in.** Add to the class tally on the board: for each prompt, Plain or Skill for "would actually use", the two job scores, and whether your prediction was right. For the advanced-topics grade, hand in a screenshot of one side-by-side pair and two or three sentences on what the skill did well and what it got wrong.

**Discuss.**

- Did the skill make the work better, or only different?
- Where did the plain version win?
- How often did the predictions come true, and does that change how you read the tally?
- The skill asks for a real fact to build on. What happened when the prompt had none?

## What to notice

- **The model's eyes are screenshots.** In every route, Claude only judges what it can render and look at. The best prompts tell it how to look, not just what to make.
- **Rules beat descriptions.** "Loop every 60 seconds" and "no image files" shaped the harbour more than "night harbour" did.
- **Small files are a trade.** Code-made art stores a recipe instead of the result, and spends computing power every frame to rebuild it.
- **The first idea is the familiar one.** Paintings, posters and names all drifted to the middle without direction. The skill makes that visible by writing the default down; it is up to you whether moving away from it was an improvement.

## What it cost

| Run | Cost | Time |
|---|---|---|
| Coffee shop, plain | $0.08 | 3 s |
| Coffee shop, with the skill | $0.13 | 10 s |

The skill run cost more because it reads its instructions and runs its seed script before answering. Posters cost more on both sides, and the skill side most, because it renders and checks the SVG. We did not measure the starter prompt in Step 2 with Claude Code's cost counter: type `/cost` in your session afterwards to see yours. The class exercise is about 10 to 14 runs per pair.

## Limits and caveats

- **One pair proves little.** Two replies to one prompt can't show that a skill improves creativity. The skill's own showcase images were picked from about a dozen runs. That's why the exercise runs several prompts and pools the class's results.
- **Not blind.** Everyone knows which side used the skill. The prediction step makes that bias visible but doesn't remove it.
- **Made-up details.** With a thin prompt, the skill invents concrete details (the 5:40 opening time) and is told to say so. Check that it did before using anything.
- **Community code.** antialgorithm is a small project by one developer. The setup script pins the commit we tested; a newer version may behave differently.
- **The computer use part is read-only here.** It needs an API key with credit and a custom setup, so the topic explains it instead of running it.

## Troubleshooting

- **`setup.sh` says `practice already has plain/ or with-skill/`.** You ran it before. Delete the old folders with `rm -rf practice` (from `demo/`) and run it again.
- **`with-skill` doesn't list antialgorithm.** Make sure you started `claude` inside `demo/practice/with-skill`, not a parent folder, and that `.claude/skills/antialgorithm/SKILL.md` exists there.
- **The poster run fails at `check.py`.** Install the Python packages: `python3 -m pip install numpy pillow cairosvg`.
- **The planet on the page says WebGL isn't available.** Turn on hardware acceleration in your browser's settings, or try another browser. The rest of the page works without it.
- **Claude says it can't take screenshots in Step 2.** Let it install Playwright when it asks (`npm install playwright` and `npx playwright install chromium`).

## Clean up

From `demo/`:

```bash
rm -rf practice
```

That removes both practice folders and the skill copy inside `with-skill`. Nothing was installed anywhere else.

## Files

| Path | What it is |
|---|---|
| `demo/art-by-code.html` | The interactive page: build loop, seeds, the shader planet, the computer use replay and the exercise |
| `demo/setup.sh` | Makes `practice/plain` and `practice/with-skill` and installs antialgorithm `766e304` into the second only |
| `sample-output/harbour/` | The starter prompt's result: `harbour.html`, Claude's screenshot script `shoot.js`, and screenshots at t=0, 20, 40 and 60 |
| `sample-output/poster/` | The festival poster with and without the skill, and a side-by-side image |

## Where to read more

- [antialgorithm on GitHub](https://github.com/mankidev/antialgorithm): the skill, its scripts and its showcase.
- [JS Paint](https://github.com/1j01/jspaint): the browser copy of MS Paint used in Step 5.
- [The Book of Shaders](https://thebookofshaders.com/): a gentle, interactive introduction to writing shaders.
- [Computer use in the Claude docs](https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool): how the tool calls in Step 5 work.

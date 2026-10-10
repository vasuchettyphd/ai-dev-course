# Week 1: What AI is

**Goal:** explain, in your own words, what a language model does when it writes: it predicts the next piece of text, one piece at a time.

**Time:** about 75 minutes. **Cost:** nothing beyond your browser.

**Tested with:** the model Qwen/Qwen2.5-0.5B (revision `060db6499f32faf8b98477b0a26969ef7d8b9987`), numbers computed 10 October 2026.

## Before you start

You need a laptop and a web browser. Nothing to install, no account, no sign-up.

This week you use the **explorer**, a single web page made for this course:

- Online: <https://vasuchettyphd.github.io/ai-dev-course/weeks/01-what-is-ai/explorer/>
- The copy in this repository: [explorer/index.html](explorer/index.html)

Every number on the page comes from a real AI model, Qwen2.5-0.5B, a small open model with about half a billion internal numbers (its makers list 0.49 billion). The numbers were worked out ahead of time and stored inside the page, so it also works downloaded, with no internet.

Keep the explorer open in one tab and this README in another. Each step below is a short explanation followed by something to try.

## Steps

### 1. AI as next-word prediction

A language model does one job: given some text, it scores every possible next piece of text. That's it. When a chatbot writes you a paragraph, it is doing this job over and over, adding one piece at a time.

The scores are probabilities. A probability is "how likely, out of 100 tries". If a weather forecast says 30% chance of rain, it means that on 100 days like today, about 30 would be rainy. When the model gives a word 6.4%, it means: in 100 tries at this sentence, about 6 would continue with that word.

**Try it.** In section 1 of the explorer, "Guessing the next word", do this for 3 sentence starts:

1. Pick a sentence start from the list.
2. Type the word you think comes next.
3. Press **Reveal**. The page shows the model's top 10 words and where your word ranked.

Leave the temperature at 1.0 for now. At 1.0 the numbers are the model's own. Here is what you'll see for a few of them:

| Sentence start | Model's top words |
|---|---|
| The best way to start a small business is to | have 6.4%, get 5.8%, find 5.5% |
| The capital of France is | Paris 31.6%, then a fill-in-the-blank line (`______`) 11.5% |
| Two plus two equals | four 22.7%, three 10.9%, five 6.0% |

Notice three things:

- **No single answer.** For the small business sentence, even the favourite word gets only 6.4%. The model spreads its bets across many reasonable words.
- **It learned from real text, including worksheets.** After "The capital of France is", the second choice is a blank line. Somewhere in what it read, that sentence was a quiz question waiting for a student to fill in.
- **Likely is not the same as true.** After "Two plus two equals", the model gives "three" 10.9% and "five" 6.0%. Together that's 16.9%, roughly 1 try in 6 picking a wrong number.

**Discussion question:** Why might the model pick a likely word that's false?

### 2. Temperature

When a model writes, it doesn't always take its favourite word. It picks at random, using the probabilities like weighted dice. **Temperature** is a dial that changes how the dice are weighted.

- **Low temperature** makes the favourite words even more favoured. The model plays it safe.
- **High temperature** flattens the differences. Unlikely words get a bigger share, so the writing gets more varied and more odd.

**Try it.** In section 1, pick "Two plus two equals" and press **Reveal**. Slide the temperature down towards 0.2 and watch "four" take over: the choices sharpen. Slide it up towards 2.0 and watch the bars even out: the choices spread, and "everything else" grows.

One honest note: only at 1.0 are the numbers the model's own. At other settings the page estimates them, as the note under the slider says.

### 3. Tokens

The model doesn't read letters or whole words. It first chops text into pieces called **tokens**. A common word is often one token. A rare word, a number or a name gets split into several.

**Try it.** In section 2 of the explorer, "How the model sees text", look at each line. Each coloured chip is one token, and a dot (`·`) marks a space at the start of a piece. Find the split that surprises you most. Some to look for:

- "strawberry" becomes 3 tokens: `str`, `aw`, `berry`.
- "Revenue grew 12.5% to $3,450,000 in Q3." is 7 words but 23 tokens, because every digit is its own token.
- "El cliente quiere un reembolso." (Spanish) is 9 tokens; "reembolso" alone is 4 of them.
- "The best way to start a small business is to" is 10 words and 10 tokens.

**Why the strawberry question trips models up.** People like to ask a chatbot "How many r's are in strawberry?" and some models get it wrong. Now you can see why: the model never sees the letters. It sees `str`, `aw`, `berry`, three chunks, and has to have learned from its reading how those chunks are spelled.

**What this means for cost.** Services that let your own code call a model, like the ones you'll use in weeks 9-11, charge by the token, for both what you send and what comes back. Numbers, unusual words and some languages use more tokens for the same idea, so they cost more and fill up the model's reading space faster.

### 4. Attention, and *Attention Is All You Need*

In 2017, eight researchers, who did the work at Google Brain and Google Research, published a paper called *Attention Is All You Need*. It appeared at NIPS 2017, one of the main conferences in AI research. The paper introduced a new design for a language model, which it named the **Transformer**.

Before this paper, many of the best models for jobs like translation read a sentence one word at a time, passing a running summary from each word to the next. That step-by-step reading is slow to train, because each step has to wait for the one before it. Those models already used **attention** as a helper: a way to look directly at any other word and decide how much each one matters. The paper's idea was to drop the step-by-step machinery entirely and rely on attention alone. That is the title: attention is all you need. The authors tested it on translating English to German and English to French, and reported that it translated better while taking much less time to train.

The model in the explorer is a Transformer too. It has 24 layers, stacked one after another, and each layer does its own round of attention.

One more thing about how this kind of model reads: it goes **left to right**. At each word, it can look back at the words before it, but never ahead.

**Try it.** Go to section 3 of the explorer, "Where the model looks". It has three parts.

**A. Make a prediction first.** Two sentences differ by one word:

- The trophy didn't fit in the suitcase because it was too **big**.
- The trophy didn't fit in the suitcase because it was too **small**.

A person knows "it" means the trophy in the first and the suitcase in the second. But remember the model reads left to right: when it reaches "it", it hasn't seen "big" or "small" yet. So its attention at "it" is exactly the same in both sentences. It can't be anything else.

What about at "big" and "small" themselves? Choose trophy or suitcase for each, then press **Reveal**. At layer 6, the layer where these words look at "trophy" the most:

| Word | trophy | suitcase |
|---|---|---|
| big | 25.4% | 17.9% |
| small | 27.9% | 16.5% |

(The page rounds these to whole numbers: 25%, 18%, 28%, 17%.) "Trophy" gets a bit more in **both** sentences. So attention is not showing which object "big" or "small" describes. The rest of the attention is spread over many other words. Attention is not a readable explanation of what the model "thinks".

**About the first word.** These numbers set the first word, "The", aside. Models park a lot of attention on the first word as a kind of resting place: at layer 6, "big" puts 52.8% of its attention there. The page hides the first word by default so you can see the rest. Tick **Include the first word** to see it.

**B. A pattern that is easy to see.** We tested a few sentences and picked the clearest one: "Paris is in France and Berlin is in". At layer 21, the last "in" gives 50.7% of its attention to "Berlin" (with the first word set aside; the page shows 51%). That helps the model predict the next word, "Germany".

**C. Explore on your own.** Pick any of the three sentences, click any word, and move the layer slider through all 24 layers. Darker shading means more attention.

Attention shows where the model looked, not proof that it understood.

### 5. Training vs. using a model

There are two very different moments in a model's life.

- **Training** happens once, before you ever meet the model. It reads a huge amount of text and, over and over, tries to predict the next token, then nudges its internal numbers to do a little better next time. The model in the explorer has about half a billion of these numbers. The big chatbots have far more.
- **Using** the model is what happens when you type a question. The numbers are now fixed. The model predicts one token, adds it to the text, predicts the next, and so on until it stops.

This is why a model doesn't "look things up". When it answers you, there is no search engine and no database inside it, only those fixed numbers, tuned on text it read in the past. If what it read was out of date or wrong, its answer can be too. A model can only check a website, a file or a calculator if someone gives it a **tool** to do that. Week 11 teaches exactly that: tools, agents and MCP.

### 6. Why models make things up

Go back to step 1. The model's job is to produce a likely next word, not a true one. Most of the time likely and true agree, because most of what it read was sensible. But "Two plus two equals" still gave "three" 10.9%. When the model doesn't have a strong answer, it still produces something fluent that sounds like the kind of thing that comes next. That is how a model can confidently invent a book that doesn't exist, a quote nobody said or a number that's off.

So you can't take a model's word for it. You have to check. Week 12, Evaluation, shows how to measure how often a model is right on the kind of task you care about, instead of trusting a few good-looking answers.

## Check it worked

You can now explain, without notes:

- What a language model does: it scores possible next tokens and picks one, again and again.
- What a token is, and why that makes the strawberry question hard and affects cost.
- Why a fluent answer can still be false, and why attention numbers don't prove the model understood.

The [assignment](assignment.md) asks you to use these ideas on problems from your own life.

## Troubleshooting

| What you see | What to do |
|---|---|
| The online page won't load | Use the copy in this repository: open [explorer/index.html](explorer/index.html) on GitHub, use the **Download raw file** button (a down-arrow icon above the file), then double-click the downloaded file to open it in your browser. It works with no internet. |
| The page looks wrong on a phone | Turn the phone sideways, or use a laptop. The explorer is easiest on a bigger screen. |

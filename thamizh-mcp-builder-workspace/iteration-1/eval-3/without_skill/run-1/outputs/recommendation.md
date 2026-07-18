# Recommendation: Building a Grounded Tamil Word-Analysis MCP

## The short answer

- **Language: Python.** It has the only mature Tamil NLP stack, the cleanest MCP server SDK, and the Unicode/text-handling libraries you need for a Brahmic script. Use the official `mcp` Python SDK (FastMCP-style decorators).
- **Data sources: curated, citable lexical and morphological resources** — a real morphological analyzer plus dictionaries (Tamil Lexicon / University of Madras, Agarathi, Wiktionary), not the model's own memory of Tamil grammar.
- **Anti-hallucination strategy: the model never produces the analysis.** The MCP tools run deterministic lookups against those resources and return structured data with citations. The LLM only orchestrates calls and phrases the result. If a word is not found, the tool says so — it does not guess.

That third point is the whole game. The rest of this document explains how to make it real.

---

## 1. Why Python (and not the alternatives)

| Option | Verdict | Reasoning |
|---|---|---|
| **Python** | **Recommended** | Mature MCP SDK; the actual Tamil NLP libraries (below) are Python-first; excellent Unicode and grapheme handling; easy to wrap CLI tools and databases as tools. |
| Node/TypeScript | Viable for the server, weak for the linguistics | The MCP TypeScript SDK is first-class, but you would shell out to Python or Java for every analysis anyway. Adds a process boundary for no benefit unless your team is JS-only. |
| Java | Only if you commit to a specific analyzer | Some classical morphological tools (e.g. finite-state transducers) ship as Java/C. You can call them from Python via subprocess; you do not need to write the server in Java. |

Python lets the **server** and the **linguistics** live in one language, which matters because the grounding logic (parse, look up, attach citation, refuse if absent) is where bugs hide.

### Tamil-specific implementation notes for whichever language

- Tamil is an abugaita-style Brahmic script. A single "letter" (உயிர்மெய், a consonant+vowel cluster) is several Unicode code points. **Never** index or slice by code point — segment by grapheme cluster. In Python use the `regex` module (`\X`) or `grapheme`; in JS use `Intl.Segmenter`.
- Normalize input to **NFC** before any lookup, and strip/standardize variant forms (e.g. legacy TSCII or TAB encodings, the two Unicode forms of certain combos). Inconsistent normalization is the #1 cause of false "not found" results.
- Handle the Tamil **digits, the aaytham (ஃ), and Grantha characters** explicitly so loanwords and Sanskrit-derived forms don't break the analyzer.

---

## 2. The data sources to use

Split sources into two layers. **Morphology** answers "how is this word built?"; **lexicon** answers "what does this root/word mean, and is it real?" You want both, and you want every answer traceable to one of them.

### Layer A — Morphological analysis (the engine)

This is what stops grammar hallucination. A morphological analyzer is a *rule- and lexicon-based* system that splits a word into root + suffixes (case, tense, person/number/gender, plural, etc.) deterministically.

1. **Open-Tamil** (`open-tamil`, PyPI) — Tamil text-processing toolkit: tokenization, letter/grapheme handling, transliteration, basic morphology helpers. Good baseline and pure-Python. Permissive license. **Start here.**
2. **A finite-state morphological analyzer (FST).** These are the gold standard for agglutinative languages like Tamil because they encode grammar as rules, not as model weights — so they cannot invent a suffix that doesn't exist.
   - **HFST / Apertium-style Tamil analyzers** — open finite-state transducers for Tamil morphology.
   - **Vaakku / TamilMorph and academic FST analyzers** — research-grade analyzers for Tamil verb and noun morphology.
   - Wrap whichever you choose as a subprocess and parse its tagged output into your schema.
3. **Stanza (Stanford NLP)** — has a Tamil model (trained on the Tamil Universal Dependencies treebank) for tokenization, lemmatization, POS tagging, and morphological features (UD feature tags). Useful as a cross-check and for sentence-level context. Note: it is statistical, so treat it as *corroboration*, not ground truth — see the confidence rules below.
4. **IndicNLP Library / AI4Bharat (IndicXlit, IndicNLP)** — strong for transliteration, script normalization, and tokenization across Indian languages including Tamil.

> Practical stance: use a **rule-based FST as the primary** morphology source (it is auditable and non-hallucinating), and a statistical model (Stanza) only to disambiguate or corroborate. Never let the statistical model be the sole source of a grammatical claim.

### Layer B — Lexicon / dictionary (meaning + existence check)

5. **Tamil Lexicon (University of Madras / Madras Tamil Lexicon)** — the authoritative historical dictionary. Digitized versions are queryable; this is your citation of record for a word's existence and senses.
6. **Agarathi (agarathi.com)** and **Tamil Virtual Academy** dictionaries — accessible, well-structured Tamil-Tamil and Tamil-English entries.
7. **Wiktionary (Tamil + English entries for Tamil words)** — dumps are downloadable, structured, and include etymology and inflection tables. Good breadth; verify against the Tamil Lexicon for authority.
8. **Tamil WordNet (IndoWordNet / AU-KBC)** — synsets, semantic relations, senses. Use for meaning, synonyms, and sense disambiguation.
9. **Sandhi / grammar rules from classical grammar (Nannūl, Tolkāppiyam-derived rule sets)** — for explaining *why* a form changes (புணர்ச்சி / sandhi). Encode these as an explicit, citable rule table, not as free-text the model recites.

### How to actually obtain and ship them

- **Download and host the data yourself** (SQLite or a small Postgres) wherever the license permits — Wiktionary dumps, WordNet, FST data files. Local data = reproducible, fast, offline, and you control the exact version you cite.
- For sources that are web-only (Agarathi, Tamil Lexicon portals), either get an offline copy where licensed or wrap them behind a cached fetch tool — but **cache and snapshot** so answers are stable.
- Record license terms per source and keep an attribution list. The Tamil Lexicon and academic analyzers have specific reuse conditions.

---

## 3. The architecture that prevents hallucination

The core principle: **the LLM is the narrator, not the linguist.** Every grammatical or lexical fact must come back from a tool that read it from a real source. Build the MCP so that the model *cannot* answer a Tamil-grammar question without calling a tool, and the tool *cannot* answer without a source hit.

### Design the tools as deterministic lookups

Expose narrow, typed tools — not one "analyze Tamil" megatool:

- `analyze_word(word)` → runs the FST/morphological analyzer; returns root, POS, and an ordered list of suffixes/features, each tagged with the rule that produced it.
- `lookup_dictionary(word_or_root)` → returns senses, gloss, etymology, **with the source name and entry ID**.
- `split_sandhi(word)` → applies the encoded sandhi rule table; returns the components and the rule reference.
- `inflect(root, features)` → generates a form from the FST (so generation is also rule-based, not invented).
- `transliterate(text, scheme)` → deterministic, for ISO 15919 / romanization.

Each tool returns **structured JSON**, and every field carries provenance.

### Make "I don't know" a first-class result

This is the single most important anti-hallucination move:

- If the analyzer returns no parse, the tool responds `{"found": false, "reason": "no analysis", "word": "..."}`. The model is instructed to relay that the word could not be analyzed — **not** to reconstruct a plausible-sounding parse.
- Distinguish **"not in source"** from **"source unavailable."** Never let a timeout silently become a confident answer.
- Attach a **confidence/source-type tag**: `rule-based` (FST/dictionary — high trust) vs `statistical` (Stanza — corroborating). Surface this so a low-confidence statistical guess is never presented as fact.

### Force grounding at the prompt/contract level

- Ship a system prompt / tool description that states: *answer Tamil linguistic questions only from tool output; if tools return no result, say so; never supply grammar, suffixes, or meanings from your own knowledge.*
- Have each tool **echo the exact source text or entry** it used, so the final answer can quote and cite (e.g. "per Madras Tamil Lexicon, entry X"). Citations are both a feature and a guardrail — a claim with no citation is, by contract, not allowed out.
- Where multiple sources disagree, return all of them with their labels and let the answer present the disagreement, rather than silently picking one.

### Validate, then trust

- Build an **eval set** of known words with hand-checked correct analyses (verbs across tenses, nouns across the eight cases, sandhi examples, loanwords, rare/classical forms). Run it on every change. Track recall (did it find real words?) and, crucially, **the rate of fabricated parses on out-of-vocabulary input** — that number should be zero.
- Add deliberate **negative tests**: nonsense strings and non-Tamil input must return `found: false`, never a confident parse.

---

## 4. Recommended starting stack (concrete)

- **Server:** Python 3.11+, official `mcp` SDK, FastMCP-style tool decorators.
- **Text layer:** `regex` (grapheme clusters), Unicode NFC normalization, Open-Tamil for tokenization/transliteration.
- **Morphology (primary, rule-based):** an HFST/Apertium Tamil FST analyzer wrapped as a subprocess; **secondary/corroborating:** Stanza Tamil model.
- **Lexicon (local, citable):** Wiktionary Tamil dump + Tamil WordNet loaded into SQLite, with the Madras Tamil Lexicon as the authority of record for existence/senses.
- **Sandhi/grammar:** an explicit, sourced rule table (Nannūl-based), exposed via `split_sandhi`/`inflect`.
- **Contract:** every tool returns JSON with `source`, `source_id`, `confidence`, and a `found` flag; system prompt forbids ungrounded linguistic claims.

### Suggested build order

1. Stand up the MCP server with one tool: `lookup_dictionary` against a local Wiktionary/WordNet SQLite. Prove citations flow end to end.
2. Add `analyze_word` backed by the FST analyzer. Wire in the `found: false` contract.
3. Add `split_sandhi` and `inflect` from the rule table.
4. Build the eval set (including negative tests) and gate every change on it.
5. Add Stanza as corroboration and the confidence tagging.

---

## Bottom line

Use **Python** with the official MCP SDK. Ground every Tamil answer in a **rule-based morphological analyzer (FST) plus citable dictionaries** (Madras Tamil Lexicon, Wiktionary, Tamil WordNet), held locally so versions are stable. Prevent hallucination not with better prompting alone but **structurally**: the model orchestrates and narrates, the tools do deterministic lookups, every fact carries a source, and "not found" is an allowed and expected answer. A chatbot hallucinates because it is the source; your MCP won't, because the sources are real, external, and cited.

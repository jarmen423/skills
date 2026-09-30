# Design principles, in plain words

A working library for diagnosing "it feels off" and explaining the fix. Each entry: what it is, the symptom that points to it, the usual fix. Use the vocabulary, define it once, and tie it to what the user noticed.

## Contents
1. Lettering and sign-painting
2. Color
3. Typography
4. Hierarchy and layout
5. Authenticity and restraint
6. Screens, print and practical limits

---

## 1. Lettering and sign-painting

**Drop shadow (on light backgrounds).** A dark offset copy of the letters behind them. Symptom: white or light letters look flat or thin on a colored panel. Fix: a crisp, hard-edged shadow in the darkest brand color, offset down-right. Skip it on very small text, where it just looks doubled.

**Block shade.** A solid offset "extrusion" of the letters in a contrasting color, the sign painter's way of adding depth. Symptom: a title lacks presence, especially on a dark background where a black shadow would vanish. Fix: stack the offset a few steps in an accent color.

**Keyline / split.** A thin outline (or gap) between the letter and its shade so they don't touch. Symptom: a light shade color blurs into light letters, or dark letters touching a red shade look muddy. Fix: a dark keyline on dark pages, a white split on light pages.

**Outline letters.** Letters defined by their outline only. Useful for secondary display; hard to read small.

## 2. Color

**Warm vs. cool blacks.** Most "brand blacks" lean warm (slightly brown) or cool (slightly blue). Symptom: a black that looked fine in small doses reads brown as a full-screen background, especially next to wood tones or red. Fix: a neutral black for large dark surfaces; keep the warm black for text and marks.

**Simultaneous contrast.** Colors change depending on what's next to them. Symptom: two reds that are "almost the same" look wrong side by side; a pale pink-red looks washed out next to a true red. Fix: one red per view, or deliberately different roles.

**Hue vs. lightness.** To make a color readable on dark, raise its lightness while keeping its hue. Symptom: a "lighter red" turns pink because saturation dropped. Fix: a true-red hue at higher lightness, checked for contrast.

**Contrast ratio.** Text needs roughly 4.5:1 against its background (3:1 for large text and UI edges). Symptom: prices or links hard to read, especially red on black. Fix: check the number; adjust lightness, not just hue.

**Accent budget.** One strong accent carries more meaning than several. Symptom: everything is colorful so nothing stands out, or everything matches the text so nothing does. Fix: one accent for "act here / look here" (buttons, prices, current state).

**Complementary pop.** Opposite colors make each other vivid (blue next to brown/orange, red next to green). Use it to make food or a key element pop; watch for unwanted associations (red + green reading as holiday).

## 3. Typography

**Voices.** Each typeface in a system should have one job: display, headings, reading, working details, handwriting. Symptom: two similar faces blur together. Fix: pick faces that differ clearly, and give each a single role.

**Hierarchy by change of voice.** A title and the items under it should differ in more than size. Symptom: a page feels flat, and the eye can't tell section from item. Fix: a different face, case or treatment for the top level.

**All caps.** Caps read well for a few words and slow reading for long lines. Symptom: long dish names or sentences in caps feel shouty and slow. Fix: caps for short titles and labels only.

**Look-alike characters.** Some faces make 1/l/I and 0/O nearly identical. Symptom: dates and prices misread on labels. Fix: a working face with distinct figures for anything numeric.

**Legibility at size.** Test text at the size it will actually be seen: 7.5 pt on a label, 16 px on a phone, a feed image at phone width. Distressed or decorative faces fail first.

## 4. Hierarchy and layout

**One signature element.** Most memorable designs have one strong idea, with everything else quiet. Symptom: several competing effects. Fix: pick the one that carries the brand and calm the rest.

**Change one variable.** When comparing options, keep everything else identical. Otherwise the user reacts to the wrong difference.

**Safe zones.** Phone apps cover parts of the screen (top profile bar, bottom reply bar, side buttons in stories and reels). Keep key content out of them.

**Minimum size and clear space.** Logos have a size below which they stop reading, and need breathing room around them. Symptom: a crowded header squeezes the logo. Fix: remove a redundant element before shrinking the logo.

**Remove duplicates.** If two controls do the same job (a header button and a bottom bar), drop one. It usually solves a space problem too.

## 5. Authenticity and restraint

**Ground it in the source.** Colors, letters and motifs sampled from the real place or object feel right in a way invented ones don't. Tell the user where each came from.

**Fake imperfection reads as a filter.** Randomly jittering every letter looks like someone trying to look handmade. Real handmade objects are imperfect in specific, structural ways (grooves, tape, a signature). Let those carry it.

**Physical objects keep their colors.** A paper receipt stays paper-colored in dark mode; a white cup stays white. Inverting everything breaks the metaphor.

**Theme metaphors.** Give each mode or context a story ("the white enamel sign over a dark window", "the awning over the shop") so later decisions have something to be judged against.

## 6. Screens, print and practical limits

**Home printers.** Mono lasers print color as gray and backgrounds as tint. Design printables on white paper, black ink first.

**Dark mode is its own design.** Automatically flipping light-mode colors rarely works. Re-decide surfaces, reds, logo treatment and emphasis for dark on purpose.

**Measure the cost before optimizing.** A web font may be 13 KB, less than one small photo. Don't trade flexibility for a saving nobody will notice.

**Placeholders over invention.** Unconfirmed prices, dates and claims go in visible `[BRACKETS]` so nobody mistakes them for decisions.
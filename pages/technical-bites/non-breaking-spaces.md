---
title: Non-breaking spaces
date: 2025-08-10
---

I learned about this from [Max Tagher](https://x.com/maxtagher?lang=en).

## The problem

There&nbsp;are some&nbsp;points on&nbsp;a webpage&nbsp;where you&nbsp;don't want&nbsp;the line&nbsp;to wrap&nbsp;between two&nbsp;words. Examples&nbsp;include units&nbsp;and numbers ("100&nbsp;km", "1&nbsp;cup"), dates ("10&nbsp;December"), and names/titles ("Dr.&nbsp;Mitch&nbsp;Eggers"). But&nbsp;if you&nbsp;use a&nbsp;regular space, a&nbsp;browser might&nbsp;wrap the&nbsp;text in&nbsp;that space.

## The solution

You&nbsp;guessed it: non-breaking&nbsp;spaces. Browsers&nbsp;have a&nbsp;special space&nbsp;character which&nbsp;looks the&nbsp;exact same&nbsp;as a&nbsp;regular space&nbsp;but won't&nbsp;break the&nbsp;line. Just&nbsp;insert `&nbsp;` instead&nbsp;of a&nbsp;space.

I've&nbsp;put non-breaking&nbsp;spaces in&nbsp;between every&nbsp;other word&nbsp;on this&nbsp;page. Resize&nbsp;your browser&nbsp;window to&nbsp;see!

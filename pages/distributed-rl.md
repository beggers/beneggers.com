---
title: Distributed reinforcement learning performance
subtitle: 2025-08-13
draft: true
---

## Introduction

## What is reinforcement learning (RL)?

Models, policies, rollouts, simulations, agents, reward functions

## Maze

<section id="maze-root">
  <div class="panel">

    <div class="controls">
      <div class="control" style="align-self: center">
        <label class="switch" title="Lights On/Off">
          <input id="maze-lights" type="checkbox" checked />
          <span>Lights <strong id="maze-lights-label">On</strong></span>
        </label>
      </div>
      <div class="legend">
        <span class="dot"></span> You
        <span class="key"></span> Key
        <span class="exit"></span> Exit
        <span class="grey"></span> Explored (lights off)
      </div>
      <div class="actions">
        <button id="new">New maze</button>
        <button id="reset" class="secondary">Reset position</button>
      </div>
    </div>

    <div class="canvas-wrap">
      <canvas id="maze-canvas" width="480" height="480" aria-label="Maze canvas" role="img"></canvas>
      <div id="maze-toast" class="toast" aria-live="polite"></div>
    </div>
    <noscript><div>Please enable JavaScript to see the interactive maze.</div></noscript>

  </div>
</section>

## A simple (synchronous) RL agent

Probably run a learner in-browser and let them interact with it

Loss based on Dijkstra's -- not used for training but lets us see the thing get better.

Lol maybe a visualization of a single node switching from sampling and grading to updating.

An aside on the type of model we're using and a link to the code.

## More complex rewards

Reward models => high variance in reward latency, often correlated with sample latency.

## Synchronous RL on multiple nodes

Actually train the maze agent on multiple logical nodes? Or maybe break into full simulatons here.

Visualization of multiple nodes going back and forth between training and not. Allow user to change step latency, reward latency, update latency, weights distribution latency.

Save a snapshot every N steps and let them watch it solve the maze

## Enter Distributed RL

Core idea: off-policy sampling. Core challenge: Then how do you update your policy?

Tradeoffs: less efficient updates per flop, but better compute saturation and wall clock time.

## Distributed RL simulation (TODO better title)

Same as "Synchronous RL on multiple nodes" above, but async.

<script src="{% protocol %}://distributed-rl.scripts.{% base_url %}"></script>

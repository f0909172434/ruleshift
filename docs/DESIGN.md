# Product and interaction design

The initial editorial direction was superseded at the user's request on 2026-09-20. The current redesign follows direct examination of the official sites below, rather than a design skill.

## References observed

- [DeepSeek homepage](https://www.deepseek.com/en/): a focused first action, generous whitespace, restrained pill controls; hovering a button expands a circular fill (public CSS uses a roughly 360 ms ease-out transform); the Get App control reveals a QR panel. The headline uses a pointer-following blend circle. The published homepage bundle contains requestAnimationFrame-driven cursor drawing, a flowing patterned background, coarse-pointer checks, visibility handling and reduced-motion/performance fallback. These behaviors were inspected in the live page and public source; the website's full implementation was not copied.
- [ChatGPT Images 2.5](https://openai.com/zh-Hant/index/introducing-chatgpt-images-2-5/): concrete examples precede detailed explanation. Example tabs change selected backgrounds with a roughly 300 ms transition. Before/after comparisons clip two images around a draggable divider, with a 44 px target, range-input keyboard support and focus styling. A direction-key test changed the visible comparison from 50/50 to 51/49. These are useful interaction patterns, not assets to reuse.

## RuleShift interpretation

The overview is now a draggable miniature lab. Two perspective policy objects show the world and remembered evidence. Moving simulated time changes A→B→A without automatically updating memory. Drag the authoritative policy into the memory object, or use the equivalent labelled button: a short transfer/scan animation marks a new observation and increments the visible read counter. Acting from the stale rule first reveals a blocked action; after synchronization the same request is correctly denied. When the original rule returns, stale restrictive memory can cause a false rejection. All outcomes are deterministic teaching examples, prominently distinguished from model evidence.

Pointer position tilts policy objects by a bounded amount. The drag target highlights only when it can accept the rule; releasing elsewhere leaves memory unchanged. A sliding selection pill, ripple originating at the pointer, and a local headline blend lens create visible feedback. Required information is not available only on hover. Source/record disclosures remain explicit.

Animations have bounded duration; pointer updates use one pending animation frame rather than a continuous loop. Pointer tracking stops on scroll/hidden pages. Reduced-motion removes positional, blur and blending effects; synchronization is immediate. Touch and keyboard users can click the policy ticket or named sync control instead of dragging, and use arrow/Home/End keys on the time control. Mobile stacks workbench columns and internal tables scroll horizontally.

The complete world and actual experiment records remain separate views. Demonstration animation never changes evidence, triggers paid inference or invents a benchmark result. Code, names and assets are RuleShift's own. No copied logos, third-party screenshots, remote fonts or decorative model-generated images are needed.

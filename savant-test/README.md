# SAVANT TEST

We want to test our nascent model for any savant traits it may have.

We are immediately to focuse on creating a training sequence that is intended to replicate the results outlined in the `unit-distance-rpoof.pdf`.

Here are the criteria we weant. We do not want the model to know anything about the proof outlined in the paper. We want to look at the proof analytically and determine exactly what sources were used for the proof. Then, we train a model to the point where it should be able to make all of the same conclusions as the original sources (this could be a fairly large corpus of work) and see if 1.) can our model make the leap to known research? i.e. Can it derive the material used for the source of a paper. and 2.) can it then use all its learning to make the same leap as in the Unit Distance proof?

In all likelihood, it will not be able to do this. However, this will give us a shortcut in insight into where our approach may need improvement or reconsideration.

If it DOES work, we want to do the same thing but for UNSOLVED problems, such as Riemman Hypothesis or anything with a cash prize associated with it in the mathematics vein where we can submit a proof in exactly the format we need it. Obviously this is a super stretch goal, but this is the trajectory we will take when the system becomes more capable.

So your first task it to thoroughly understand the argument, determine what source material would need to be mastered to get to that point, then create a curriculum to achieve the source material proofs (or arguments, lemmas, etc. whatever concepts they contain). We may even want to confound it with some true math facts that don't belong to the category of the paper's solution, just to make sure that they are properly ignored or not utilized. Or maybe they happen to be useful, but as long as we keep results honest.

We'll see if it can match the source material's conclusions, then we will see if it matches the actual paper itself. If it doesn't, we can try a second approach where we teach it full mastery of the source material and re-test whether it could then come up with a similar proof to the one in the paper. The slower approach will help us catch any gotchas before the real test and see if foundational learning is working as we want.

To be clear, we want not only for the system to produce a proof (or claim it doesn't know how to figure it out), but for the reasoning chain to be inspectable so that we can document how it came to its conclusions.

I want you to pull out all the stops for this one!

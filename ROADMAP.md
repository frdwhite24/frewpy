# Frewpy Roadmap

This roadmap is intended to outline a 6-12 month forecast of development work for frewpy. Each stage holds core development targets which will be broken down into issues to be completed. Each issue will refer directly to the numbered core target and all information to complete that issue will be contained within the description of it. Once all issues and therefore core targets are completed for the stage, there will be a version release and development will progress onto the next stage.

## Stage 1 [v1.0.0]

✅ [1] establish a scalable and extendable structure for the core library

❌ [2] convert all initial release functionality into new core structure so that users do not lose out by updating versions. This includes: outputting envelopes, plotting results (comparing design cases at each stage), analysing a model, saving a model, calculating soil pressures, getting water pressures.

✅ [3] make the workflow clear with error handling so that if users load in a Frew .fwd model file that they need to convert it to a json with the function. Write this module.

❌ [4] establish 100% unit-testing coverage on the functionality of the library.

✅ [5] complete the documentation to a good quality so that it allows people to, at a minimum, know how to contribute, understand what's changed between versions, know how to get started with the library, and can search all the source code in a plain text manner. This includes linking the key markdown files with the restructured text.

👇

## Stage 2 [v1.1.0]

❌ [6] Extend the functionality to set soil properties, allowing iteration through ranges.

❌ [7] Increase the number of examples in the examples directory so users can easily pick the library up and extend the functionality.

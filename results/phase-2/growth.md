# 20Q growth — E2.2 learning sequence (empty start -> 200 games)
sampled every 25 games (n_games=200)

| game | coverage_mean | unknown_cells_remaining | sometimes | dimensions | assertions |
|-----:|--------------:|------------------------:|----------:|-----------:|-----------:|
| 0 | 0.0000 | 1490 | 0 | 0 | 0 |
| 25 | 0.0134 | 1422 | 5 | 2 | 236 |
| 50 | 0.0470 | 1359 | 8 | 4 | 472 |
| 75 | 0.0872 | 1304 | 15 | 5 | 696 |
| 100 | 0.1678 | 1270 | 20 | 6 | 944 |
| 125 | 0.2215 | 1245 | 25 | 6 | 1171 |
| 150 | 0.2550 | 1203 | 35 | 6 | 1392 |
| 175 | 0.3087 | 1172 | 40 | 6 | 1621 |
| 200 | 0.3490 | 1150 | 43 | 6 | 1857 |

## Final dashboard sample
# 20Q growth dashboard

- Sampled: `2026-08-20T17:51:25+00:00`
- Assertions: **1857**
- Status mix: candidate: 552, established: 1305
- Exception states: requires_context: 43
- 'sometimes' cells: **43**
- Dimensions expanded by contradiction: **6** — dim:can_carry_person, dim:has_engine, dim:has_wheels, dim:is_green, dim:lives_in_water, dim:manufactured

## Coverage per concept (verified / encountered)

- Mean: **0.3490** · Min: **0.0000**
- Concepts at 0.0000: 97 of 149

| concept | coverage |
|---------|---------:|
| adult_man | 0.0000 |
| adult_woman | 1.0000 |
| airplane | 0.0000 |
| ant | 1.0000 |
| apartment | 1.0000 |
| apple | 1.0000 |
| baby | 0.0000 |
| bacon | 1.0000 |
| bamboo | 1.0000 |
| banana | 0.0000 |
| bat | 0.0000 |
| beach | 0.0000 |
| bee | 1.0000 |
| beef | 1.0000 |
| bicycle | 1.0000 |
| blanket | 0.0000 |
| boat | 1.0000 |
| book | 0.0000 |
| bottle | 0.0000 |
| bowl | 0.0000 |
| bread | 0.0000 |
| bridge | 0.0000 |
| broccoli | 0.0000 |
| burger | 0.0000 |
| bus | 0.0000 |
| butterfly | 0.0000 |
| cactus | 0.0000 |
| cake | 1.0000 |
| canoe | 0.0000 |
| car | 1.0000 |
| carrot | 0.0000 |
| cat | 1.0000 |
| chair | 0.0000 |
| cheese | 1.0000 |
| chicken | 1.0000 |
| chicken_meat | 1.0000 |
| child | 1.0000 |
| chocolate | 0.0000 |
| church | 0.0000 |
| city | 0.0000 |
| clock | 1.0000 |
| coffee | 0.0000 |
| computer | 1.0000 |
| cookie | 1.0000 |
| corn | 0.0000 |
| cow | 0.0000 |
| crab | 0.0000 |
| cup | 0.0000 |
| daisy | 1.0000 |
| desert | 0.0000 |
| dog | 1.0000 |
| dolphin | 1.0000 |
| door | 0.0000 |
| duck | 1.0000 |
| eagle | 0.0000 |
| egg | 1.0000 |
| elderly_man | 0.0000 |
| elderly_woman | 0.0000 |
| elephant | 0.0000 |
| fern | 1.0000 |
| ferry | 0.0000 |
| forest | 0.0000 |
| forklift | 0.0000 |
| frog | 0.0000 |
| giraffe | 0.0000 |
| grass | 1.0000 |
| hammer | 0.0000 |
| helicopter | 0.0000 |
| honey | 0.0000 |
| horse | 0.0000 |
| hospital | 0.0000 |
| house | 1.0000 |
| ice_cream | 1.0000 |
| ivy | 1.0000 |
| kayak | 0.0000 |
| key | 0.0000 |
| lamp | 0.0000 |
| laptop | 0.0000 |
| lemon | 0.0000 |
| lettuce | 1.0000 |
| library | 0.0000 |
| lion | 0.0000 |
| lock | 0.0000 |
| milk | 1.0000 |
| minivan | 0.0000 |
| mirror | 0.0000 |
| monkey | 1.0000 |
| motorcycle | 0.0000 |
| mountain | 1.0000 |
| museum | 0.0000 |
| mushroom | 0.0000 |
| needle | 0.0000 |
| oak_tree | 0.0000 |
| octopus | 1.0000 |
| office | 0.0000 |
| park | 0.0000 |
| pasta | 0.0000 |
| penguin | 0.0000 |
| phone | 0.0000 |
| pig | 1.0000 |
| pillow | 0.0000 |
| pine_tree | 1.0000 |
| pizza | 0.0000 |
| plate | 0.0000 |
| potato | 0.0000 |
| rabbit | 1.0000 |
| race_car | 0.0000 |
| rice | 0.0000 |
| rice_plant | 0.0000 |
| rose | 0.0000 |
| sailboat | 1.0000 |
| salad | 1.0000 |
| salmon | 0.0000 |
| school | 0.0000 |
| scissors | 0.0000 |
| scooter | 0.0000 |
| screwdriver | 1.0000 |
| shark | 0.0000 |
| sheep | 0.0000 |
| shopping_cart | 0.0000 |
| shrimp | 1.0000 |
| snake | 1.0000 |
| sparrow | 0.0000 |
| stadium | 1.0000 |
| steak | 1.0000 |
| submarine | 0.0000 |
| subway | 0.0000 |
| sunflower | 1.0000 |
| sushi | 0.0000 |
| table | 1.0000 |
| taxi | 0.0000 |
| tea | 0.0000 |
| teenager | 0.0000 |
| tiger | 1.0000 |
| toddler | 0.0000 |
| tomato | 0.0000 |
| tractor | 1.0000 |
| train | 0.0000 |
| truck | 0.0000 |
| tulip | 0.0000 |
| tuna | 0.0000 |
| tunnel | 0.0000 |
| van | 1.0000 |
| village | 0.0000 |
| whale | 0.0000 |
| wheat | 1.0000 |
| wheelchair | 0.0000 |
| window | 1.0000 |
| wrench | 0.0000 |

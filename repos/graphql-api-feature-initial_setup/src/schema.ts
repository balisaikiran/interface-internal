import { typeDef as workflow } from './workflow/schema.js';
import { typeDef as fub } from './fub/schema.js';
import { typeDef as opp } from './opp/schema.js';
import {mergeTypeDefs} from '@graphql-tools/merge'

export const typeDefs = mergeTypeDefs([workflow, fub, opp])

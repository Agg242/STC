/* MIT License
 *
 * Copyright (c) 2021 Tyge Løvset, NORCE, www.norceresearch.no
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
#ifndef CSET_H_INCLUDED
#define CSET_H_INCLUDED

// Unordered set - implemented as closed hashing with linear probing and no tombstones.
/*
#include <stc/cset.h>
#include <stdio.h>

using_cset(sx, int);    // Set of int

int main(void) {
    cset_sx s = cset_sx_init();
    cset_sx_insert(&s, 5);
    cset_sx_insert(&s, 8);

    c_foreach (i, cset_sx, s)
        printf("set %d\n", *i.ref);
    cset_sx_del(&s);
}
*/

#include "cmap.h"

/* cset: */
#define using_cset(...) \
    c_MACRO_OVERLOAD(using_cset, __VA_ARGS__)

#define using_cset_2(X, Key) \
    using_cset_4(X, Key, c_default_equals, c_default_hash)
#define using_cset_4(X, Key, keyEquals, keyHash) \
    using_cset_6(X, Key, keyEquals, keyHash, c_trivial_del, c_trivial_fromraw)
#define using_cset_5(X, Key, keyEquals, keyHash, keyDel) \
    using_cset_6(X, Key, keyEquals, keyHash, keyDel, c_no_clone)
#define using_cset_6(X, Key, keyEquals, keyHash, keyDel, keyClone) \
    using_cset_8(X, Key, keyEquals, keyHash, keyDel, keyClone, c_trivial_toraw, Key)

#define using_cset_8(X, Key, keyEqualsRaw, keyHashRaw, keyDel, keyFromRaw, keyToRaw, RawKey) \
    _using_CHASH(X, cset_, Key, Key, keyEqualsRaw, keyHashRaw, \
                    @@, @@, @@, void, \
                    keyDel, keyFromRaw, keyToRaw, RawKey)

/* cset_str: */
#define using_cset_str() \
    _using_CHASH_strkey(str, cset_, cstr_t, @@, @@, @@, void)

#define SET_ONLY_cset_(...) __VA_ARGS__
#define MAP_ONLY_cset_(...)
#define KEY_REF_cset_(vp)   (vp)

#endif

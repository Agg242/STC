#include <stc/cstr.h>
#include <stc/cmap.h>
#include <stc/clist.h>
#include <stc/carr.h>

void check_destroy(float* v) {printf("destroy %g\n", *v);}

declare_CArr(f, float, check_destroy); // normally omit the last argument - float type need no destroy.
declare_CList(t2, CArr2_f, carr2_f_destroy, c_noCompare);
declare_CMap(il, int, CList_t2, clist_t2_destroy);
declare_CMap_str(sm, CMap_il, cmap_il_destroy);

int main() {
    int xdim = 4, ydim = 6;
    int x = 1, y = 5, tableKey = 42;
    const char* strKey = "first";
    CMap_sm theMap = cmap_init;

    { // Construct.
        CArr2_f table = carr2_f_make(ydim, xdim, 0.f);
        printf("table: (%zu, %zu)\n", carr2_ydim(table), carr2_xdim(table));
        CList_t2 tableList = clist_init;
        CMap_il listMap = cmap_init;
        
        // Put in some data.
        carr2_f_data(table, y)[x] = 3.1415927; // table[y][x]
        clist_t2_pushBack(&tableList, table);
        cmap_il_put(&listMap, tableKey, tableList);
        cmap_sm_put(&theMap, strKey, listMap);
    }
    { // Access the data entry
        CArr2_f table = clist_back(cmap_il_find(&cmap_sm_find(&theMap, strKey)->value, tableKey)->value);
        printf("value (%d, %d) is: %f\n", y, x, carr2_f_value(table, y, x));
    }

    cmap_sm_destroy(&theMap); // free up the whole shebang!
}
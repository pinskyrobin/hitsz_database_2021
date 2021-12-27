#include <stdio.h>
#include <stdlib.h>
#include "extmem.h"
#include <string.h>
typedef struct tuple {
    int a;
    int b;
} tuple;

void int2str(unsigned char *dst, int a) {
    int len;
    int base;
    if (a == 0) {
        len = 0;
        base = 0;
    } else if (a < 10) {
        len = 1;
        base = 1;
    } else if (a < 100){
        len = 2;
        base = 10;
    } else if (a < 1000){
        len = 3;
        base = 100;
    } else {
        len = 4;
        base = 1000;
    }
    for (int i = 0; i < len; i++) {
        dst[i] = a / base + '0';
        a %= base;
        base /= 10;
    }
    for (int i = len; i < 4; i++) {
        dst[i] = 0;
    }
}

int str2int(const unsigned char *src) {
    char str[5];
    str[4] = 0;
    for (int k = 0; k < 4; k++) {
        str[k] = *(src + k);
    }
    return atoi(str);
}

tuple get(const unsigned char *blk, int index) {
    int i;
    tuple t;
    t.a = 0;
    t.b = 0;
    char first[4], second[4];
    for (i = 0; i < 4; i++) {
        first[i] = *(blk + index * 8 + i);
        second[i] = *(blk + index * 8 + 4 + i);
    }
    t.a = str2int(first);
    t.b = str2int(second);
    return t;
}

void set_from_blk(const unsigned char *blk, unsigned char *res_blk, int blk_idx, int res_blk_idx) {
    int i;
    for (i = 0; i < 8; i++) {
        *(res_blk + res_blk_idx * 8 + i) = *(blk + blk_idx * 8 + i);
    }
}

void set_from_tuple(unsigned char *blk, int index, tuple t) {
    int i;

    int a = t.a;
    int b = t.b;
    unsigned char str_a[4], str_b[4];
    int2str(str_a, a);
    int2str(str_b, b);

    for (i = 0; i < 4; i++) {
        *(blk + index * 8 + i) = str_a[i];
    }
    for (i = 4; i < 8; i++) {
        *(blk + index * 8 + i) = str_b[i - 4];
    }

}

void write(unsigned char *res_blk, Buffer *buf, int *output) {
    tuple t = {*output + 1, 0};
    set_from_tuple(res_blk, 7, t);
    if (writeBlockToDisk(res_blk, *output, buf) != 0){
        perror("Writing Block Failed!\n");
        return ;
    }
    printf("结果写入磁盘:%d\n", *output);
    *output = *output + 1;
    memset(res_blk, 0, 64);
}

void write_tuple(unsigned char *res_blk, int *index, tuple t, Buffer *buf, int *res_blk_num) {
    set_from_tuple(res_blk, (*index)++, t);
    if (*index == 7) {
        write(res_blk, buf, res_blk_num);
        freeBlockInBuffer(res_blk, buf);
        res_blk = getNewBlockInBuffer(buf);
        memset(res_blk, 0, 64);
        *index = 0;
    }
}

void inner_sort(int start, int end, Buffer *buf) {
    // 每一组的磁盘块数(最后一组很可能不为6)
    int blk_cnt;

    unsigned char *blk;
    unsigned char *blks[6];
    // 组数
    int group_num = (end - start) / 6 + 1;

    // 当前处理的磁盘块号
    int curr_blk_num = start;
    // 写回时的磁盘块号
    int write_blk_num = start;

    // 待比较两元组的所属磁盘块号和块内索引
    // tuple_of_blk_num 取值范围 : [0, 6]
    // tuple_idx 取值范围 : [0, 6]
    int tuple_of_blk_num1, tuple_idx1;
    int tuple_of_blk_num2, tuple_idx2;

    // 分别存放冒泡排序中两个要比较的数
    tuple a, b;

    // 分组排序
    for (int i = 0; i < group_num; i++) {
        blk_cnt = 0;
        for (; blk_cnt < 6 && curr_blk_num <= end; curr_blk_num++, blk_cnt++) {
            blks[blk_cnt] = readBlockFromDisk(curr_blk_num, buf);
        }
        for (int j = 0; j < blk_cnt * 7 - 1; j++) {
            tuple_of_blk_num1 = j / 7;
            tuple_idx1 = j % 7;
            for (int k = j + 1; k < blk_cnt * 7; k++) {
                tuple_of_blk_num2 = k / 7;
                tuple_idx2 = k % 7;
                a = get(blks[tuple_of_blk_num1], tuple_idx1);
                b = get(blks[tuple_of_blk_num2], tuple_idx2);
                if (a.a > b.a) {
                    set_from_tuple(blks[tuple_of_blk_num1], tuple_idx1, b);
                    set_from_tuple(blks[tuple_of_blk_num2], tuple_idx2, a);
                }
            }
        }

        // 数据写回
        for (int l = 0; l < blk_cnt; l++) {
            blk = blks[l];
            write(blk, buf, &write_blk_num);
        }
    }
}


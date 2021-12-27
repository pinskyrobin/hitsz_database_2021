#include <string.h>
#include "utils.h"

#define FINISHED 4001

void problem_1(int start, int end, int key, int res_blk_num) {
    Buffer buf;
    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    unsigned char *blk;
    unsigned char *res_blk;
    int res_blk_index = 0;
    int blk_num;
    int blk_index;
    int res_cnt = 0;

    tuple t;

    printf("--------------------\n");
    printf("基于线性搜索的选择算法\n");
    printf("--------------------\n");

    res_blk = getNewBlockInBuffer(&buf);

    for (blk_num = start; blk_num <= end; blk_num++) {
        printf("读入数据块%d\n", blk_num);
        if ((blk = readBlockFromDisk(blk_num, &buf)) == NULL) {
            perror("Reading Block Failed!\n");
            return;
        }

        for (blk_index = 0; blk_index < 7; blk_index++) {
            t = get(blk, blk_index);
            if (t.a == key) {
                res_cnt++;
                printf("(C = %d,D = %d)\n", t.a, t.b);
                set_from_blk(blk, res_blk, blk_index, res_blk_index++);
            }
            if (res_blk_index == 7 || (blk_num == end && blk_index == 6)) {
                write(res_blk, &buf, &res_blk_num);
                res_blk_index = 0;
            }
        }
        freeBlockInBuffer(blk, &buf);
    }

    freeBuffer(&buf);

    printf("\n满足条件的元组一共 %d 个\n", res_cnt);
    printf("IO读写一共%lu次\n", buf.numIO);
    printf("\n");
}

void problem_2(int start, int end, int res_blk_num) {
    Buffer buf;
    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    unsigned char *blk;
    // 组数
    int group_num = (end - start) / 6 + 1;

    // 内存中的比较块
    unsigned char *cmp_blk;
    // 写入磁盘的数据块
    unsigned char *res_blk;
    // 比较块中每个数据块的来源及其索引
    unsigned char *cmp_blks[8];
    int cmp_blks_idx[8];

    // 记录每一组当前处理的磁盘块号
    int group_idx[8];

    // 写回内存块中的块内元组及其索引
    int tuple_idx = 0;
    tuple t, min_t;

    // 当前最小值及其索引
    int min_idx, min_val = 0;

    // 内排序
    inner_sort(start, end, &buf);

    // 第 7 块内存,用作比较
    cmp_blk = getNewBlockInBuffer(&buf);
    memset(cmp_blk, 0, 64);
    // 第 8 块内存,用作写回
    res_blk = getNewBlockInBuffer(&buf);
    memset(res_blk, 0, 64);

    t.a = FINISHED;
    t.b = FINISHED;
    for (int i = 0; i < 8; i++) {
        set_from_tuple(cmp_blk, i, t);
    }

    // 初始化,将每组第一个磁盘块读入内存
    for (int i = 0; i < group_num; i++) {
        group_idx[i] = start + i * 6;
        blk = readBlockFromDisk(group_idx[i], &buf);
        cmp_blks[i] = blk;
        t = get(blk, 0);
        set_from_tuple(cmp_blk, i, t);
        cmp_blks_idx[i] = 1;
    }

    while (1) {
        // 获取排序内存块里元组的最小值及其索引
        min_idx = 0;
        min_val = FINISHED;
        for (int i = 0; i < 8; i++) {
            t = get(cmp_blk, i);
            if (t.a < min_val) {
                min_val = t.a;
                min_t.a = t.a;
                min_t.b = t.b;
                min_idx = i;
            }
        }

        // 没有需要排序的元素,退出
        if (min_val == FINISHED) {
            break;
        }

        write_tuple(res_blk, &tuple_idx, min_t, &buf, &res_blk_num);

        // 读最小元素所在块的下一个元组
        t = get(cmp_blks[min_idx], cmp_blks_idx[min_idx]++);

        // 如果 cmp_blks[min_idx] 这一内存块有下一个元组
        if (t.a != 0 && cmp_blks_idx[min_idx] < 8) {
            set_from_tuple(cmp_blk, min_idx, t);
        }

            // 如果已经是最后一个元组了,就看还有没有其他磁盘块
        else {

            // 如果有
            if ((group_idx[min_idx] - start + 1) % 6 != 0 &&
                group_idx[min_idx] != end) {
                freeBlockInBuffer(cmp_blks[min_idx], &buf);
                blk = readBlockFromDisk(++group_idx[min_idx], &buf);
                cmp_blks[min_idx] = blk;
                t = get(blk, 0);
                set_from_tuple(cmp_blk, min_idx, t);
                cmp_blks_idx[min_idx] = 1;
            }

                // 如果没有,排序结束
            else {
                t.a = FINISHED;
                t.b = FINISHED;
                set_from_tuple(cmp_blk, min_idx, t);
            }
        }
    }

    freeBuffer(&buf);
}

void problem_3(int target) {
    printf("------------------------------\n");
    printf("基于索引的关系选择算法 S.C=130:\n");
    printf("------------------------------\n");

    Buffer buf;
    unsigned char *blk;
    unsigned char *res_blk;
    int res_blk_index = 0;
    int target_cnt = 0;

    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    int index_blk_num = 350;
    int target_blk_num_min = 0;
    int target_blk_num_max = 0;

    tuple t;

    /** === 建立索引 START === **/
    printf("建立索引中...\n");
    int res_blk_num = 350;
    res_blk = getNewBlockInBuffer(&buf);
    // 将每个数据块的第一个元素作为元组的第一个元素
    // 数据块的坐标作为第二个元素
    // 存入索引块中
    for (int i = 0; i < 32; i++) {
        blk = readBlockFromDisk(317 + i, &buf);
        t = get(blk, 0);
        freeBlockInBuffer(blk, &buf);
        t.b = 317 + i;
        set_from_tuple(res_blk, res_blk_index++, t);
        if (res_blk_index == 7) {
            write(res_blk, &buf, &res_blk_num);
            freeBlockInBuffer(res_blk, &buf);
            res_blk = getNewBlockInBuffer(&buf);
            memset(res_blk, 0, 64);
            res_blk_index = 0;
        }
    }
    write(res_blk, &buf, &res_blk_num);
    printf("建立索引所用IO次数为 %lu\n", buf.numIO);
    printf("索引建立完毕!\n");
    freeBuffer(&buf);
    /** === 建立索引 END === **/

    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    for (int i = 0; i < 5; i++) {
        printf("读入索引块 %d\n", index_blk_num);
        blk = readBlockFromDisk(index_blk_num++, &buf);
        for (int j = 0; j < 7; j++) {
            t = get(blk, j);
            if (t.a < target) {
                target_blk_num_min = t.b;
            } else if (t.a > target) {
                target_blk_num_max = t.b;
                break;
            }
        }
        freeBlockInBuffer(blk, &buf);
        if (target_blk_num_max == t.b) {
            break;
        }
    }

    res_blk = getNewBlockInBuffer(&buf);
    res_blk_index = 0;
    res_blk_num = 101;
    for (int i = target_blk_num_min; i < target_blk_num_max; i++) {
        blk = readBlockFromDisk(i, &buf);
        printf("读入数据块 %d\n", i);
        for (int j = 0; j < 7; j++) {
            t = get(blk, j);
            if (t.a == target) {
                target_cnt++;
                printf("(X=%d, Y=%d)\n", t.a, t.b);
                set_from_tuple(res_blk, res_blk_index++, t);
                if (res_blk_index == 7) {
                    write(res_blk, &buf, &res_blk_num);
                    res_blk_index = 0;
                }
            }
        }
        freeBlockInBuffer(blk, &buf);
    }

    write(res_blk, &buf, &res_blk_num);

    freeBuffer(&buf);

    printf("一共找到%d个符合要求的元组\n", target_cnt);
    printf("IO读写一共%lu次\n", buf.numIO);
    printf("\n");
}

void problem_4(int start_R, int end_R, int start_S, int end_S, int res_blk_num) {
    printf("------------------------------\n");
    printf("基于排序的连接操作算法\n");
    printf("------------------------------\n");

    Buffer buf;
    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    // 结果元组的个数
    int res_cnt = 0;

    // R S 以及 写回块
    unsigned char *blk_R;
    unsigned char *blk_S;
    unsigned char *res_blk = getNewBlockInBuffer(&buf);

    // 当前操作的 R S 块号及索引
    int blk_R_num = start_R;
    int blk_S_num = start_S;
    int blk_R_index = 0;
    int blk_S_index = 0;

    // 结果块索引及临时元组
    int res_blk_index = 0;
    tuple tup_R, tup_S;

    // R 块元组相等的集合里第一个元组的块号及索引,以及其组内第一个元素的值
    int curr_blk_R_num = start_R;
    int curr_blk_index = 0;
    int val_R = 0;
    // 当前操作的 S 块内元组的第一个元素的值
    int val_S = 0;

    for (; blk_S_num <= end_S; blk_S_num++) {
        blk_S = readBlockFromDisk(blk_S_num, &buf);
        for (blk_S_index = 0; blk_S_index < 7; blk_S_index++) {
            tup_S = get(blk_S, blk_S_index);

            // 如果相等,回退 R
            if (val_S == tup_S.a) {
                blk_R_num = curr_blk_R_num;
                blk_R_index = curr_blk_index;
            }
                // 否则,更新 val_S
            else {
                val_S = tup_S.a;
            }

            for (; blk_R_num <= end_R; blk_R_num++) {
                blk_R = readBlockFromDisk(blk_R_num, &buf);
                for (; blk_R_index < 7; blk_R_index++) {
                    tup_R = get(blk_R, blk_R_index);

                    if (tup_R.a > tup_S.a) break;
                    if (tup_R.a == tup_S.a) {
                        if (val_R != tup_R.a) {
                            curr_blk_R_num = blk_R_num;
                            curr_blk_index = blk_R_index;
                            val_R = tup_R.a;
                        }
                        write_tuple(res_blk, &res_blk_index, tup_R, &buf, &res_blk_num);
                        write_tuple(res_blk, &res_blk_index, tup_S, &buf, &res_blk_num);
                        res_cnt++;
                    }
                }

                if (tup_R.a <= tup_S.a) blk_R_index = 0;
                freeBlockInBuffer(blk_R, &buf);
                memset(blk_R, 0, 64);

                if (tup_R.a > tup_S.a) {
                    break;
                }
            }
        }

        freeBlockInBuffer(blk_S, &buf);
        memset(blk_S, 0, 64);
    }

    if (res_blk_index != 0) {
        write(res_blk, &buf, &res_blk_num);
        freeBlockInBuffer(res_blk, &buf);
        res_blk = getNewBlockInBuffer(&buf);
        memset(res_blk, 0, 64);
    }

    freeBuffer(&buf);

    printf("总共连接次数:%d\n", res_cnt);
    printf("\n");
}

void problem_5_1(int start_R, int end_R, int start_S, int end_S, int res_blk_num) {
    printf("------------------------------\n");
    printf("基于排序的连接操作算法: 交操作\n");
    printf("------------------------------\n");

    Buffer buf;
    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    // 结果元组的个数
    int res_cnt = 0;

    // R S 以及 写回块
    unsigned char *blk_R;
    unsigned char *blk_S;
    unsigned char *res_blk = getNewBlockInBuffer(&buf);

    // 当前操作的 R S 块号及索引
    int blk_R_num = start_R;
    int blk_S_num = start_S;
    int blk_R_index = 0;
    int blk_S_index = 0;

    // 结果块索引及临时元组
    int res_blk_index = 0;
    tuple tup_R, tup_S;

    // R 块元组相等的集合里第一个元组的块号及索引,以及其组内第一个元素的值
    int curr_blk_R_num = start_R;
    int curr_blk_index = 0;
    int val_R = 0;
    // 当前操作的 S 块内元组的第一个元素的值
    int val_S = 0;

    /*** dup : 重复模式状态
     * dup 为 0 时,正常
     * dup 为 1 时,表示当前 S 块元组值与上一个元组相等
     *      这时只要观察是否有与该元组相同的 R 块元组即可
     *          --> 如果有,将 dup 置为 2,在切换下一个 S 块元组前将其写回
     *          --> 否则说明 R 块内没有与其相同的元组,不写回
     * dup 在当前 S 块元组值与上一个元组不等时置 0.
     */
    int dup;

    for (; blk_S_num <= end_S; blk_S_num++) {
        blk_S = readBlockFromDisk(blk_S_num, &buf);
        for (blk_S_index = 0; blk_S_index < 7; blk_S_index++) {
            tup_S = get(blk_S, blk_S_index);

            // 如果相等,回退 R,进入重复模式
            if (val_S == tup_S.a) {
                dup = 1;
                blk_R_num = curr_blk_R_num;
                blk_R_index = curr_blk_index;
            }
                // 否则,更新 val_S,退出重复模式
            else {
                val_S = tup_S.a;
                dup = 0;
            }

            for (; blk_R_num <= end_R; blk_R_num++) {
                blk_R = readBlockFromDisk(blk_R_num, &buf);
                for (; blk_R_index < 7; blk_R_index++) {
                    tup_R = get(blk_R, blk_R_index);

                    if (tup_R.a > tup_S.a) break;
                    if (tup_R.a == tup_S.a) {
                        if (val_R != tup_R.a) {
                            curr_blk_R_num = blk_R_num;
                            curr_blk_index = blk_R_index;
                            val_R = tup_R.a;
                        }
                    }

                    /** 有相同元组,我们只要这样的元组!!!
                     * 之所以没有 break 退出,
                     * 是为了当 S 块下一元组值比当前的大时,
                     * 可以迅速找到 R 块开始扫描的位置,
                     * 避免之前 R 块元组重复扫描
                     */
                    if (tup_R.a == tup_S.a && tup_R.b == tup_S.b) {
                        printf("(X = %d, Y = %d)\n", tup_R.a, tup_R.b);
                        dup = 2;
                    }
                }

                if (tup_R.a <= tup_S.a) blk_R_index = 0;
                freeBlockInBuffer(blk_R, &buf);
                memset(blk_R, 0, 64);

                if (tup_R.a > tup_S.a) {
                    break;
                }
            }

            if (dup == 2) {
                res_cnt++;
                write_tuple(res_blk, &res_blk_index, tup_S, &buf, &res_blk_num);
            }
        }

        freeBlockInBuffer(blk_S, &buf);
        memset(blk_S, 0, 64);
    }

    if (res_blk_index != 0) {
        write(res_blk, &buf, &res_blk_num);
        freeBlockInBuffer(res_blk, &buf);
        res_blk = getNewBlockInBuffer(&buf);
        memset(res_blk, 0, 64);
    }
    printf("R和S的交集一共有%d个元组\n", res_cnt);

    freeBuffer(&buf);
}

void problem_5_2(int start_R, int end_R, int start_S, int end_S, int res_blk_num) {
    printf("------------------------------\n");
    printf("基于排序的连接操作算法: 并操作\n");
    printf("------------------------------\n");

    Buffer buf;
    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    // 结果元组的个数
    int res_cnt = 0;

    // R S 以及 写回块
    unsigned char *blk_R;
    unsigned char *blk_S;
    unsigned char *res_blk = getNewBlockInBuffer(&buf);

    // 当前操作的 R S 块号及索引
    int blk_R_num = start_R;
    int blk_S_num = start_S;
    int blk_R_index = 0;
    int blk_S_index = 0;

    // 结果块索引及临时元组
    int res_blk_index = 0;
    tuple tup_R, tup_S;

    // R 块元组相等的集合里第一个元组的块号及索引,以及其组内第一个元素的值
    int curr_blk_R_num = start_R;
    int curr_blk_index = 0;
    int val_R = 0;
    // 当前操作的 S 块内元组的第一个元素的值
    int val_S = 0;

    /*** dup : 重复模式
     * dup 为 0 时,正常
     * dup 为 1 时,表示当前 S 块元组值与上一个相等
     *      这时只要观察是否有与该元组相同的 R 块元组即可
     *          --> 如果有,将 dup 置为 2,在切换下一个 S 块元组前不将其写回
     *          --> 否则说明 R 块内没有与其相同的元组,这时写回
     * dup 在当前 S 块元组值与上一个不等时置 0.
     */
    int dup;

    for (; blk_S_num <= end_S; blk_S_num++) {
        blk_S = readBlockFromDisk(blk_S_num, &buf);
        for (blk_S_index = 0; blk_S_index < 7; blk_S_index++) {
            tup_S = get(blk_S, blk_S_index);

            // 如果相等,回退 R,进入重复模式
            if (val_S == tup_S.a) {
                dup = 1;
                blk_R_num = curr_blk_R_num;
                blk_R_index = curr_blk_index;
            }
                // 否则,更新 val_S,退出重复模式
            else {
                val_S = tup_S.a;
                dup = 0;
            }

            for (; blk_R_num <= end_R; blk_R_num++) {
                blk_R = readBlockFromDisk(blk_R_num, &buf);
                for (; blk_R_index < 7; blk_R_index++) {
                    tup_R = get(blk_R, blk_R_index);

                    if (tup_R.a > tup_S.a) break;
                    if (tup_R.a == tup_S.a) {
                        if (val_R != tup_R.a) {
                            curr_blk_R_num = blk_R_num;
                            curr_blk_index = blk_R_index;
                            val_R = tup_R.a;
                        }
                    }
                    if (dup) {
                        if (tup_R.a == tup_S.a && tup_R.b == tup_S.b) {
                            dup = 2;
                        }
                        continue;
                    }
                    if (tup_R.a == tup_S.a && tup_R.b == tup_S.b) continue;
                    res_cnt++;
                    write_tuple(res_blk, &res_blk_index, tup_R, &buf, &res_blk_num);
                }

                if (tup_R.a <= tup_S.a) blk_R_index = 0;
                freeBlockInBuffer(blk_R, &buf);
                memset(blk_R, 0, 64);

                if (tup_R.a > tup_S.a) {
                    break;
                }
            }

            if (dup != 2) {
                res_cnt++;
                write_tuple(res_blk, &res_blk_index, tup_S, &buf, &res_blk_num);
            }
        }

        freeBlockInBuffer(blk_S, &buf);
        memset(blk_S, 0, 64);
    }

    if (res_blk_index != 0) {
        write(res_blk, &buf, &res_blk_num);
        freeBlockInBuffer(res_blk, &buf);
        res_blk = getNewBlockInBuffer(&buf);
        memset(res_blk, 0, 64);
    }
    printf("R和S的并集一共有%d个元组\n", res_cnt);

    freeBuffer(&buf);
}

void problem_5_3(int start_R, int end_R, int start_S, int end_S, int res_blk_num) {
    printf("------------------------------\n");
    printf("基于排序的连接操作算法: 差操作\n");
    printf("------------------------------\n");

    Buffer buf;
    if (!initBuffer(520, 64, &buf)) {
        perror("Buffer Initialization Failed!\n");
        return;
    }

    // 结果元组的个数
    int res_cnt = 0;

    // R S 以及 写回块
    unsigned char *blk_R;
    unsigned char *blk_S;
    unsigned char *res_blk = getNewBlockInBuffer(&buf);

    // 当前操作的 R S 块号及索引
    int blk_R_num = start_R;
    int blk_S_num = start_S;
    int blk_R_index = 0;
    int blk_S_index = 0;

    // 结果块索引及临时元组
    int res_blk_index = 0;
    tuple tup_R, tup_S;

    // R 块元组相等的集合里第一个元组的块号及索引,以及其组内第一个元素的值
    int curr_blk_R_num = start_R;
    int curr_blk_index = 0;
    int val_R = 0;
    // 当前操作的 S 块内元组的第一个元素的值
    int val_S = 0;

    /*** dup : 重复模式状态
     * dup 为 0 时,正常
     * dup 为 1 时,表示当前 S 块元组值与上一个元组相等
     *      这时只要观察是否有与该元组相同的 R 块元组即可
     *          --> 如果有,将 dup 置为 2,在切换下一个 S 块元组前不将其写回
     *          --> 否则说明 R 块内没有与其相同的元组,这时写回
     * dup 在当前 S 块元组值与上一个元组不等时置 0.
     */
    int dup;

    for (; blk_S_num <= end_S; blk_S_num++) {
        blk_S = readBlockFromDisk(blk_S_num, &buf);
        for (blk_S_index = 0; blk_S_index < 7; blk_S_index++) {
            tup_S = get(blk_S, blk_S_index);

            // 如果相等,回退 R,进入重复模式
            if (val_S == tup_S.a) {
                dup = 1;
                blk_R_num = curr_blk_R_num;
                blk_R_index = curr_blk_index;
            }
                // 否则,更新 val_S,退出重复模式
            else {
                val_S = tup_S.a;
                dup = 0;
            }

            for (; blk_R_num <= end_R; blk_R_num++) {
                blk_R = readBlockFromDisk(blk_R_num, &buf);
                for (; blk_R_index < 7; blk_R_index++) {
                    tup_R = get(blk_R, blk_R_index);

                    if (tup_R.a > tup_S.a) break;
                    if (tup_R.a == tup_S.a) {
                        if (val_R != tup_R.a) {
                            curr_blk_R_num = blk_R_num;
                            curr_blk_index = blk_R_index;
                            val_R = tup_R.a;
                        }
                    }

                    /** 有相同元组,这样的 S 块元组不能要!!!
                     * 之所以没有 break 退出,
                     * 是为了当 S 块下一元组值比当前的大时,
                     * 可以迅速找到 R 块开始扫描的位置,
                     * 避免之前 R 块元组重复扫描
                     */
                    if (tup_R.a == tup_S.a && tup_R.b == tup_S.b) {
                        dup = 2;
                    }
                }

                if (tup_R.a <= tup_S.a) blk_R_index = 0;
                freeBlockInBuffer(blk_R, &buf);
                memset(blk_R, 0, 64);

                if (tup_R.a > tup_S.a) {
                    break;
                }
            }

            if (dup != 2) {
                res_cnt++;
                write_tuple(res_blk, &res_blk_index, tup_S, &buf, &res_blk_num);
            }
        }

        freeBlockInBuffer(blk_S, &buf);
        memset(blk_S, 0, 64);
    }

    if (res_blk_index != 0) {
        write(res_blk, &buf, &res_blk_num);
        freeBlockInBuffer(res_blk, &buf);
        res_blk = getNewBlockInBuffer(&buf);
        memset(res_blk, 0, 64);
    }
    printf("R和S的差集(S-R)一共有%d个元组\n", res_cnt);

    freeBuffer(&buf);
}


int main() {
    problem_1(17, 48, 130, 100);

    printf("------------------------------\n");
    printf("关系 R 排序\n");
    printf("------------------------------\n");
    printf("\n");
    problem_2(1, 16, 301);
    printf("------------------------------\n");
    printf("关系 S 排序\n");
    printf("------------------------------\n");
    printf("\n");
    problem_2(17, 48, 317);

    problem_3(130);

    problem_4(301, 316, 317, 348, 200);

    problem_5_1(301, 316, 317, 348, 400);

    problem_5_2(301, 316, 317, 348, 500);

    problem_5_3(301, 316, 317, 348, 600);
}

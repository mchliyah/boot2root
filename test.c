
void phase_6(char *param_1)

{
  int *piVar1;
  int iVar2;
  undefined1 *puVar3;
  int *piVar4;
  int iV    ar5;
  undefined1 *local_38;
  int *local_34;
  int local_30 [5];
  int local_1c [6];
  
  local_38 = node1;
  read_six_numbers(param_1,(int)local_1c);
  iVar5 = 0;
  do {
    iVar2 = iVar5;
    if (5 < local_1c[iVar5] - 1U) {
      explode_bomb();
    }
    while (iVar2 = iVar2 + 1, iVar2 < 6) {
      if (local_1c[iVar5] == local_1c[iVar2]) {
        explode_bomb();
      }
    }
    iVar5 = iVar5 + 1;
  } while (iVar5 < 6);
  iVar5 = 0;
  do {
    iVar2 = 1;
    puVar3 = local_38;
    if (1 < local_1c[iVar5]) {
      do {
        puVar3 = *(undefined1 **)(puVar3 + 8);
        iVar2 = iVar2 + 1;
      } while (iVar2 < local_1c[iVar5]);
    }
    local_30[iVar5 + -1] = (int)puVar3;
    iVar5 = iVar5 + 1;
  } while (iVar5 < 6);
  iVar5 = 1;
  piVar4 = local_34;
  do {
    piVar1 = (int *)local_30[iVar5 + -1];
    piVar4[2] = (int)piVar1;
    iVar5 = iVar5 + 1;
    piVar4 = piVar1;
  } while (iVar5 < 6);
  piVar1[2] = 0;
  iVar5 = 0;
  do {
    if (*local_34 < *(int *)local_34[2]) {
      explode_bomb();
    }
    local_34 = (int *)local_34[2];
    iVar5 = iVar5 + 1;
  } while (iVar5 < 5);
  return;
}
import { create } from "zustand";
import { ISpool } from "../spools/model";

export const ItemTypes = {
  SPOOL: "spool",
  CONTAINER: "spool-container",
};

export interface DragItem {
  index: number;
}

export interface SpoolDragItem extends DragItem {
  spool: ISpool;
}

export interface ContainerDragItem extends DragItem {
  title: string;
}

interface CurrentDraggedSpool {
  draggedSpoolId: string;
  setDraggedSpoolId: (spoolid: string) => void;
}

export const useCurrentDraggedSpool = create<CurrentDraggedSpool>((set) => ({
  draggedSpoolId: "",
  setDraggedSpoolId: (spoolid: string) => set({ draggedSpoolId: spoolid }),
}));

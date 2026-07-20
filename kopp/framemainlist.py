#!/usr/bin/env python3

from collections import OrderedDict

import wx
import wx.dataview


class MainListViewData:
    """store data for the main list (columns name and width"""

    column_info = OrderedDict([
        ("Date", 150),
        ("HR", 80),
        ("A", 80),
        ("VAC", 80),
        ("Tags", 150),
        ("Comment", 200),
    ])


class FrameMainListModel(wx.dataview.DataViewIndexListModel):
    def __init__(self):
        wx.dataview.DataViewIndexListModel.__init__(self, 0)
        self.rows = []

    def GetColumnCount(self):
        return len(MainListViewData.column_info)

    def GetColumnType(self, column):
        return "string"

    def GetValueByRow(self, row, column):
        return self.rows[row]["values"][column]

    def SetValueByRow(self, value, row, column):
        self.rows[row]["values"][column] = value
        return True

    def GetAttrByRow(self, row, column, attr):
        if column in (1, 2, 3) and self.rows[row]["negative_columns"].get(column, False):
            attr.SetColour(wx.RED)
            return True
        return False

    def append_item(self, values, data):
        self.rows.append(self._make_row(values, data))
        self.RowAppended()

    def delete_item(self, row):
        del self.rows[row]
        self.RowDeleted(row)

    def delete_all_items(self):
        self.rows.clear()
        self.Reset(0)

    def set_text_value(self, value, row, column):
        self.rows[row]["values"][column] = value
        self.rows[row]["negative_columns"] = self._get_negative_columns(self.rows[row]["values"])
        self.RowChanged(row)

    def set_item_data(self, row, data):
        self.rows[row]["data"] = data

    def get_item_data(self, row):
        return self.rows[row]["data"]

    def _make_row(self, values, data):
        return {
            "values": list(values),
            "data": data,
            "negative_columns": self._get_negative_columns(values),
        }

    def _get_negative_columns(self, values):
        return {
            column: values[column].startswith("-")
            for column in (1, 2, 3)
            if column < len(values)
        }


class FrameMainListView(wx.dataview.DataViewCtrl):
    """Main records list."""

    def __init__(self, parent, identifier):
        wx.dataview.DataViewCtrl.__init__(
            self,
            parent,
            identifier,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.dataview.DV_MULTIPLE | wx.dataview.DV_ROW_LINES,
        )
        self.parent = parent
        self.m_frame_view = None
        self.m_img_path = None
        self.m_model = FrameMainListModel()
        self.AssociateModel(self.m_model)

        for column, (my_category, my_width) in enumerate(MainListViewData.column_info.items()):
            self.AppendTextColumn(my_category, column, width=my_width)

    def AppendItem(self, values, data):
        self.m_model.append_item(values, data)

    def DeleteItem(self, row):
        self.m_model.delete_item(row)

    def DeleteAllItems(self):
        self.m_model.delete_all_items()

    def GetItemCount(self):
        return len(self.m_model.rows)

    def GetSelectedItemsCount(self):
        return len(self.GetSelections())

    def GetSelectedRow(self):
        selection = self.GetSelection()
        if not selection.IsOk():
            return wx.NOT_FOUND
        return self.m_model.GetRow(selection)

    def RowToItem(self, row):
        return self.m_model.GetItem(row)

    def GetItemData(self, item):
        return self.m_model.get_item_data(self.m_model.GetRow(item))

    def SetItemData(self, item, data):
        self.m_model.set_item_data(self.m_model.GetRow(item), data)

    def SetTextValue(self, value, row, column):
        self.m_model.set_text_value(value, row, column)

    def GetAllTextValues(self):
        return [list(row["values"]) for row in self.m_model.rows]

        # self.Bind(wx.dataview.EVT_DATAVIEW_ITEM_ACTIVATED, self.on_comments)
        # self.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.on_selection_change)
        #
        # # Bind Ctrl+Up/Down events
        # accel_entries = [
        #     wx.AcceleratorEntry(wx.ACCEL_CTRL, wx.WXK_UP, wx.NewIdRef()),
        #     wx.AcceleratorEntry(wx.ACCEL_CTRL, wx.WXK_DOWN, wx.NewIdRef())
        # ]
        # accel_table = wx.AcceleratorTable(accel_entries)
        # self.SetAcceleratorTable(accel_table)
        # self.Bind(wx.EVT_MENU, self.on_select_previous_valid, id=accel_entries[0].GetCommand())
        # self.Bind(wx.EVT_MENU, self.on_select_next_valid, id=accel_entries[1].GetCommand())

    # def InvertSelection(self):
    #     for index in range(self.GetItemCount()):
    #         if self.IsRowSelected(index) is False:
    #             self.SelectRow(index)
    #         else:
    #             self.UnselectRow(index)
    #
    # def add_item(self, data: ImageData):
    #     if not data:
    #         return
    #     self.m_imgdata.append(data)
    #     list_id = len(self.m_imgdata) - 1
    #     self.AppendItem([data.get_date_str(), data.get_time_str(), data.get_short_filename(), "", "", ""], list_id)
    #
    # def on_selection_change(self, event):
    #     if not self.m_frame_view or not self.m_img_path:
    #         return
    #
    #     if self.GetSelectedItemsCount() != 1:
    #         return
    #
    #     # get imagedata
    #     row_id = self.GetSelectedRow()
    #     list_id = self.GetItemData(self.RowToItem(row_id))
    #     img_data = self.m_imgdata[list_id]
    #     self.m_frame_view.set_image(img_data)
    #
    # def on_delete_items(self, event):
    #     if self.GetSelectedItemsCount() == 0:
    #         return
    #     for selected_item in self.GetSelections():
    #         # get row for item
    #         row_id = self.ItemToRow(selected_item)
    #         list_id = self.GetItemData(selected_item)
    #         self.m_imgdata[list_id].m_delete = True
    #         self.SetTextValue("X", row_id, 3)
    #
    # def on_restore_items(self, event):
    #     if self.GetSelectedItemsCount() == 0:
    #         return
    #     for selected_item in self.GetSelections():
    #         row_id = self.ItemToRow(selected_item)
    #         list_id = self.GetItemData(selected_item)
    #         self.m_imgdata[list_id].m_delete = False
    #         self.SetTextValue("", row_id, 3)
    #
    # def on_comments(self, event):
    #     if self.GetSelectedItemsCount() != 1:
    #         return
    #
    #     selected_item = self.GetSelection()
    #     row_id = self.ItemToRow(selected_item)
    #     list_id = self.GetItemData(selected_item)
    #
    #     # display a TextEntryDialog for writing a comment
    #     dlg = wx.TextEntryDialog(self, 'Enter a comment:', 'Comment',
    #                              self.m_imgdata[list_id].m_comment)
    #     if dlg.ShowModal() == wx.ID_OK:
    #         self.m_imgdata[list_id].m_comment = dlg.GetValue()
    #         self.SetTextValue(dlg.GetValue(), row_id, 4)
    #     dlg.Destroy()
    #
    # def get_unique_selected_item(self):
    #     if self.GetSelectedItemsCount() != 1:
    #         return None
    #     selected_item = self.GetSelection()
    #     row_id = self.ItemToRow(selected_item)
    #     list_id = self.GetItemData(selected_item)
    #     return self.m_imgdata[list_id]
    #
    # def get_filenames(self, selected_only: bool = False):
    #     filenames = []
    #     for i in range(self.GetItemCount()):
    #         if selected_only and not self.IsRowSelected(i):
    #             continue
    #         filenames.append(self.GetTextValue(i, 2))
    #     return filenames
    #
    # def update_list(self):
    #     self.DeleteAllItems()
    #     for index, item in enumerate(self.m_imgdata):
    #         delete_str = ""
    #         if item.m_delete:
    #             delete_str = "X"
    #         self.AppendItem([item.get_date_str(), item.get_time_str(), item.get_short_filename(),
    #                          delete_str, item.m_comment, item.m_info], index)
    #
    # def set_text_value(self, value, row_id, column_id):
    #     self.SetValue(value, row_id, column_id)
    #
    # def get_not_deleted_indexes(self):
    #     not_deleted_indexes = []
    #     for index, item in enumerate(self.m_imgdata):
    #         if not item.m_delete:
    #             not_deleted_indexes.append(index)
    #     return not_deleted_indexes
    #
    # def on_select_next_valid(self, event):
    #     if self.GetSelectedItemsCount() != 1:
    #         return
    #     selected_item = self.GetSelection()
    #     row_id = self.ItemToRow(selected_item)
    #     list_id = self.GetItemData(selected_item)
    #     for index, item in enumerate(self.m_imgdata[list_id+1:], list_id+1):
    #         if not item.m_delete:
    #             self.SelectRow(index)
    #             self.UnselectRow(row_id)
    #             self.on_selection_change(None)
    #             return
    #
    # def on_select_previous_valid(self, event):
    #     if self.GetSelectedItemsCount() != 1:
    #         return
    #     selected_item = self.GetSelection()
    #     row_id = self.ItemToRow(selected_item)
    #     list_id = self.GetItemData(selected_item)
    #     for index in range(list_id - 1, -1, -1):
    #         if not self.m_imgdata[index].m_delete:
    #             self.SelectRow(index)
    #             self.UnselectRow(row_id)
    #             self.on_selection_change(None)
    #             return

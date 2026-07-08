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


class FrameMainListView(wx.dataview.DataViewListCtrl):
    """
    Class for the data view
    """

    def __init__(self, parent, identifier):
        wx.dataview.DataViewListCtrl.__init__(self, parent, identifier, wx.DefaultPosition, wx.DefaultSize,
                                              wx.dataview.DV_MULTIPLE | wx.dataview.DV_ROW_LINES)
        """Constructor for DataView"""
        self.parent = parent
        self.m_frame_view = None
        self.m_img_path = None
        #self.m_imgdata: list[ImageData] = []

        # create the columns
        for my_category, my_width in MainListViewData.column_info.items():
            self.AppendTextColumn(my_category, width=my_width)

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

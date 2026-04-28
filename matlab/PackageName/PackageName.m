classdef PackageName < handle
    % PackageName - Main data processing class.
    %
    % Wraps a dataset and provides methods for filtering and aggregation.
    % Supports both numeric arrays and struct arrays.

    properties
        data        % The input data (numeric array or struct array)
        metadata    % Struct with column_names and row_count
    end

    methods
        function obj = PackageName(data, column_names)
            % Initialize the processor with data.
            %
            % Args:
            %   data: Numeric array or struct array.
            %   column_names: Optional cell array of column names.

            if nargin < 2 || isempty(column_names)
                column_names = {};
            end

            obj.data = data;
            obj.metadata = struct(...
                'column_names', column_names, ...
                'row_count', length(data));
        end

        function filtered = filterData(obj, column, value, operator)
            % Filter data by condition.
            %
            % Args:
            %   column: Column name (for struct data) or ignored (for numeric).
            %   value: Value to compare.
            %   operator: One of '==', '~=', '>', '<', '>=', '<='.
            %
            % Returns:
            %   New PackageName with filtered data.

            filtered_data = filterData(obj.data, column, value, operator);
            filtered = PackageName(filtered_data, obj.metadata.column_names);
        end

        function filtered = filterRange(obj, column, min_val, max_val)
            % Filter data by range.
            %
            % Args:
            %   column: Column name (for struct data) or ignored (for numeric).
            %   min_val: Minimum value (inclusive).
            %   max_val: Maximum value (inclusive).
            %
            % Returns:
            %   New PackageName with filtered data.

            filtered_data = filterRange(obj.data, column, min_val, max_val);
            filtered = PackageName(filtered_data, obj.metadata.column_names);
        end

        function result = sumAgg(obj, column)
            % Sum of values.
            if nargin < 2, column = ''; end
            result = sum_agg(obj.data, column);
        end

        function result = meanAgg(obj, column)
            % Average of values.
            if nargin < 2, column = ''; end
            result = mean_agg(obj.data, column);
        end

        function result = countAgg(obj, column)
            % Count of non-null values.
            if nargin < 2, column = ''; end
            result = count_agg(obj.data, column);
        end

        function result = minAgg(obj, column)
            % Minimum value.
            if nargin < 2, column = ''; end
            result = min_agg(obj.data, column);
        end

        function result = maxAgg(obj, column)
            % Maximum value.
            if nargin < 2, column = ''; end
            result = max_agg(obj.data, column);
        end

        function result = summary(obj, column)
            % Get summary statistics.
            %
            % Returns:
            %   Struct with count, sum, mean, min, max.

            if nargin < 2, column = ''; end
            result = struct(...
                'count', count_agg(obj.data, column), ...
                'sum', sum_agg(obj.data, column), ...
                'mean', mean_agg(obj.data, column), ...
                'min', min_agg(obj.data, column), ...
                'max', max_agg(obj.data, column));
        end
    end
end
